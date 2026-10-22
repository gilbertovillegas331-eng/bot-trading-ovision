# engines/confluence_engine.py
from models.signal_models import TradeSignal, Confluence
from engines.smc_engine import SMCEngine
from datetime import datetime

class ConfluenceEngine:
    def __init__(self, df_htf, df_ltf, symbol):
        self.symbol = symbol
        self.htf = SMCEngine(df_htf)
        self.ltf = SMCEngine(df_ltf)
        self.current_price = df_ltf['close'].iloc[-1]
        
    def analyze(self):
        confluences = []
        
        # 1. Sesgo HTF (Temporalidad Mayor)
        _, htf_bias = self.htf.detect_swings_and_structure()
        if htf_bias:
            confluences.append(Confluence(
                factor="Sesgo Macro (HTF)",
                description=f"La estructura en temporalidad mayor es {htf_bias.upper()}.",
                weight=2
            ))
            
        # 2. Eventos LTF (Temporalidad Menor - CHoCH)
        ltf_events, ltf_bias = self.ltf.detect_swings_and_structure()
        recent_choch = [e for e in ltf_events if e[0] == "CHoCH" and e[2] > len(self.ltf.df) - 20]
        if recent_choch:
            direction_choch = recent_choch[-1][1]
            confluences.append(Confluence(
                factor="CHoCH Reciente",
                description=f"Cambio de carácter en temporalidad menor hacia {direction_choch.upper()}.",
                weight=1
            ))

        # 3. FVG Activo
        fvgs = self.ltf.detect_fvgs()
        active_fvg = next((f for f in fvgs if f['bottom'] <= self.current_price <= f['top']), None)
        if active_fvg:
            confluences.append(Confluence(
                factor="Fair Value Gap (FVG)",
                description=f"El precio está en un desequilibrio (FVG) {active_fvg['type']} entre {active_fvg['bottom']:.5f} y {active_fvg['top']:.5f}.",
                weight=1
            ))

        # 4. Order Block Activo
        obs = self.ltf.detect_order_blocks(ltf_events)
        active_ob = next((o for o in obs if o['bottom'] <= self.current_price <= o['top']), None)
        if active_ob:
            confluences.append(Confluence(
                factor="Order Block (OB)",
                description=f"El precio reacciona en un bloque de órdenes {active_ob['type']}.",
                weight=1
            ))

        # --- REGLAS DE DECISIÓN ---
        if len(confluences) >= 3 and htf_bias == ltf_bias:
            
            # REGLA DE PROTECCIÓN SINTÉTICOS
            simbolo_mayus = self.symbol.upper()
            
            # Activos SOLO de VENTA (Crash, Bear y StepRise)
            if "C " in simbolo_mayus or "BEAR" in simbolo_mayus or "STEPRISE" in simbolo_mayus:
                direction = "SHORT" 
                confluences.append(Confluence(
                    factor="Protección Índice Bajista",
                    description="El activo es de caída (Crash/Bear/StepRise). Solo se permiten ventas.",
                    weight=2
                ))
            # Activos SOLO de COMPRA (Boom, Bull y StepDrop)
            elif "B " in simbolo_mayus or "BULL" in simbolo_mayus or "STEPDROP" in simbolo_mayus:
                direction = "LONG" 
                confluences.append(Confluence(
                    factor="Protección Índice Alcista",
                    description="El activo es de subida (Boom/Bull/StepDrop). Solo se permiten compras.",
                    weight=2
                ))
            else:
                # Para Forex, STP, Fortune, FlipRand, etc.
                direction = "LONG" if htf_bias == "bull" else "SHORT"
            
            # Cálculo de SL y TP básicos (usando el ATR del LTF)
            atr = self.ltf.df['ATR'].iloc[-1]
            if direction == "LONG":
                sl = self.current_price - (atr * 1.5)
                tp = self.current_price + (atr * 3.0)
            else:
                sl = self.current_price + (atr * 1.5)
                tp = self.current_price - (atr * 3.0)
            signal = TradeSignal(
                symbol=self.symbol,
                direction=direction,
                entry_price=self.current_price,
                stop_loss=sl,
                take_profit=tp,
                risk_percent=0.5,
                timestamp=datetime.now(),
                confluences=confluences
            )
            return signal
            
        return None 