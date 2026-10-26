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
        
        _, htf_bias = self.htf.detect_swings_and_structure()
        if htf_bias:
            confluences.append(Confluence("Sesgo Macro (HTF)", f"La estructura en temporalidad mayor es {htf_bias.upper()}.", 2))
            
        ltf_events, ltf_bias = self.ltf.detect_swings_and_structure()
        
        recent_breaks = [e for e in ltf_events if e[0] in ["CHoCH", "BOS"] and e[2] > len(self.ltf.df) - 15]
        if recent_breaks:
            tipo_break = recent_breaks[-1][0]
            direccion_break = recent_breaks[-1][1]
            confluences.append(Confluence(f"Rompimiento ({tipo_break})", f"Estructura rota hacia {direccion_break.upper()}.", 2))

        fvgs = self.ltf.detect_fvgs()
        active_fvg = next((f for f in fvgs if f['bottom'] <= self.current_price <= f['top']), None)
        if active_fvg:
            confluences.append(Confluence("Fair Value Gap (FVG)", f"El precio está en un desequilibrio (FVG) {active_fvg['type']}.", 1))

        obs = self.ltf.detect_order_blocks(ltf_events)
        active_ob = next((o for o in obs if o['bottom'] <= self.current_price <= o['top']), None)
        if active_ob:
            confluences.append(Confluence("Order Block (OB)", f"Reacción en bloque {active_ob['type']}.", 1))

        sweeps = self.ltf.detect_liquidity_sweep()
        recent_sweep = next((s for s in sweeps if s['idx'] > len(self.ltf.df) - 5), None)
        if recent_sweep:
            confluences.append(Confluence("Liquidez", f"Barrido de liquidez {recent_sweep['type']}.", 1))

        patron = self.ltf.detect_candle_patterns(len(self.ltf.df) - 1)
        if patron:
            confluences.append(Confluence("Patrón de Vela", f"Confirmación de {patron}.", 1))

        max_htf = self.htf.df['high'].max()
        min_htf = self.htf.df['low'].min()
        nivel_50 = (max_htf + min_htf) / 2
        if self.current_price < nivel_50:
            confluences.append(Confluence("Zona", "Precio en Descuento (Discount).", 1))
        else:
            confluences.append(Confluence("Zona", "Precio en Prima (Premium).", 1))

        if len(confluences) >= 3 and htf_bias == ltf_bias:
            simbolo_mayus = self.symbol.upper()
            
            if "C " in simbolo_mayus or "BEAR" in simbolo_mayus or "STEPRISE" in simbolo_mayus:
                direction = "SHORT" 
                confluences.append(Confluence("Protección Bajista", "Crash/Bear/StepRise. Solo ventas.", 2))
            elif "B " in simbolo_mayus or "BULL" in simbolo_mayus or "STEPDROP" in simbolo_mayus:
                direction = "LONG" 
                confluences.append(Confluence("Protección Alcista", "Boom/Bull/StepDrop. Solo compras.", 2))
            else:
                direction = "LONG" if htf_bias == "bull" else "SHORT"
            
        direction = "LONG" if htf_bias == "bull" else "SHORT"
        atr = self.ltf.df['ATR'].iloc[-1]

        # --- MODELO 1: FIBONACCI Y ORDEN LIMITE ---
        try:
            obs = self.ltf.detect_order_blocks(ltf_events)
        except Exception:
            obs = []
        
        limit_price = self.current_price
        
        if obs:
            ob_activo = obs[-1]
            ob_low = ob_activo.get('bottom', self.current_price)
            ob_high = ob_activo.get('top', self.current_price)
            
            if direction == "LONG":
                limit_price = ob_high - ((ob_high - ob_low) * 0.618)
                sl = ob_low - 15.0 
                tp = limit_price + (atr * 3.0)
            else:
                limit_price = ob_low + ((ob_high - ob_low) * 0.618)
                sl = ob_high + 15.0 
                tp = limit_price - (atr * 3.0)
        else:
            if direction == "LONG":
                sl = self.current_price - (atr * 1.5)
                tp = self.current_price + (atr * 3.0)
            else:
                sl = self.current_price + (atr * 1.5)
                tp = self.current_price - (atr * 3.0)
        # --- FIN MODELO 1 ---
            return TradeSignal(self.symbol, direction, limit_price, sl, tp, 0.5, datetime.now(), confluences)
            
        return None
