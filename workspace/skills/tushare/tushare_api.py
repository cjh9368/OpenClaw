#!/usr/bin/env python3
"""
Tushare Stock Data API
Usage: python3 tushare_api.py <command> [args]

Commands:
  daily <ts_code> [start_date] [end_date] - Get daily stock data
  info <ts_code> - Get stock basic info
  trade_cal - Get trading calendar
  limit [trade_date] - Get limit up/down stocks statistics
  test - Test API connection
"""

import sys
import json
import requests
from datetime import datetime, timedelta

# API Configuration
TOKEN = "828abf5aa2217e5f0d0ab35b0e57f0441149775885cdd7ec7588bac36c04"
HTTP_URL = "http://lianghua.nanyangqiankun.top"

def make_request(api_name, params=None):
    """Make API request to Tushare"""
    if params is None:
        params = {}
    
    payload = {
        "api_name": api_name,
        "token": TOKEN,
        "params": params
    }
    
    try:
        response = requests.post(
            HTTP_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 0:
            return {"error": result.get("msg", "Unknown error")}
        
        return result
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {str(e)}"}

def get_daily(ts_code, start_date=None, end_date=None):
    """Get daily stock data"""
    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    if start_date is None:
        # Default to last 30 days
        start = datetime.now() - timedelta(days=30)
        start_date = start.strftime("%Y%m%d")
    
    params = {
        "ts_code": ts_code,
        "start_date": start_date,
        "end_date": end_date
    }
    
    return make_request("daily", params)

def get_stock_info(ts_code):
    """Get stock basic information"""
    params = {"ts_code": ts_code}
    return make_request("stock_basic", params)

def get_trade_cal(exchange="SSE", start_date=None, end_date=None):
    """Get trading calendar"""
    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    if start_date is None:
        start = datetime.now() - timedelta(days=30)
        start_date = start.strftime("%Y%m%d")
    
    params = {
        "exchange": exchange,
        "start_date": start_date,
        "end_date": end_date,
        "is_open": "1"
    }
    
    return make_request("trade_cal", params)

def get_limit_list(trade_date=None):
    """Get limit up/down stocks for a trade date"""
    if trade_date is None:
        # Use yesterday if today hasn't closed yet
        now = datetime.now()
        if now.hour < 15:
            trade_date = (now - timedelta(days=1)).strftime("%Y%m%d")
        else:
            trade_date = now.strftime("%Y%m%d")
    
    params = {"trade_date": trade_date}
    return make_request("limit_list_d", params)

def format_limit_output(data, trade_date):
    """Format limit up/down data for display"""
    if "error" in data:
        return f"❌ 错误：{data['error']}"
    
    if "data" not in data or "items" not in data["data"]:
        return "❌ 无数据返回"
    
    fields = data["data"].get("fields", [])
    items = data["data"]["items"]
    
    limit_idx = fields.index('limit') if 'limit' in fields else -1
    name_idx = fields.index('name') if 'name' in fields else -1
    close_idx = fields.index('close') if 'close' in fields else -1
    pct_chg_idx = fields.index('pct_chg') if 'pct_chg' in fields else -1
    
    up_limit = 0
    down_limit = 0
    up_stocks = []
    down_stocks = []
    
    for item in items:
        if limit_idx >= 0:
            limit_type = str(item[limit_idx]).upper()
            name = item[name_idx] if name_idx >= 0 else 'N/A'
            close = item[close_idx] if close_idx >= 0 else 0
            pct_chg = item[pct_chg_idx] if pct_chg_idx >= 0 else 0
            
            if limit_type == 'U':  # 涨停
                up_limit += 1
                up_stocks.append({'name': name, 'close': close, 'pct_chg': pct_chg})
            elif limit_type == 'D':  # 跌停
                down_limit += 1
                down_stocks.append({'name': name, 'close': close, 'pct_chg': pct_chg})
    
    output = []
    output.append("╔════════════════════════════════════════════════════════════╗")
    output.append("║              📊 A 股涨跌停统计                              ║")
    output.append(f"║  交易日：{trade_date}                                      ║")
    output.append("╠════════════════════════════════════════════════════════════╣")
    output.append(f"║  🔴 涨停家数：{up_limit:<42} ║")
    output.append(f"║  🟢 跌停家数：{down_limit:<42} ║")
    output.append(f"║  总计：{up_limit + down_limit:<46} ║")
    output.append("╠════════════════════════════════════════════════════════════╣")
    
    if up_stocks:
        output.append("║  涨停股前 5:                                           ║")
        for stock in up_stocks[:5]:
            name = stock['name'][:10].ljust(10)
            output.append(f"║    • {name}  收盘:{stock['close']:.2f}  涨幅:{stock['pct_chg']:.2f}%".ljust(58) + "║")
    
    if down_stocks:
        output.append("║  跌停股：                                              ║")
        for stock in down_stocks:
            name = stock['name'][:10].ljust(10)
            output.append(f"║    • {name}  收盘:{stock['close']:.2f}  跌幅:{stock['pct_chg']:.2f}%".ljust(58) + "║")
    
    output.append("╚════════════════════════════════════════════════════════════╝")
    
    return "\n".join(output), {"up_limit": up_limit, "down_limit": down_limit, "total": up_limit + down_limit}

def test_api():
    """Test API connection"""
    result = make_request("trade_cal", {"exchange": "SSE", "start_date": "20240101", "end_date": "20240107", "is_open": "1"})
    return result

def format_daily_output(data):
    """Format daily data for display"""
    if "error" in data:
        return f"❌ 错误：{data['error']}"
    
    if "data" not in data or "items" not in data["data"]:
        return "❌ 无数据返回"
    
    fields = data["data"].get("fields", [])
    items = data["data"]["items"]
    
    if not items:
        return "📭 暂无数据"
    
    # Create table header
    output = []
    output.append("╔════════════════════════════════════════════════════════════╗")
    output.append("║                    📈 股票行情数据                          ║")
    output.append("╠════════════════════════════════════════════════════════════╣")
    
    # Show latest data
    latest = items[0]  # Most recent
    output.append(f"║  代码：{ts_code:<48} ║")
    
    # Map common fields
    field_map = {
        "trade_date": "日期",
        "close": "收盘",
        "open": "开盘",
        "high": "最高",
        "low": "最低",
        "vol": "成交量",
        "amount": "成交额",
        "pct_chg": "涨跌幅%"
    }
    
    for i, field in enumerate(fields):
        if field in field_map:
            value = latest[i] if i < len(latest) else "N/A"
            if isinstance(value, float):
                value = f"{value:.2f}"
            output.append(f"║  {field_map[field]}：{str(value):<42} ║")
    
    output.append("╠════════════════════════════════════════════════════════════╣")
    output.append(f"║  共 {len(items)} 条记录                                    ║")
    output.append("╚════════════════════════════════════════════════════════════╝")
    
    return "\n".join(output)

def main():
    global ts_code  # For format_daily_output
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "test":
        print("🔌 测试 API 连接...\n")
        result = test_api()
        if "error" in result:
            print(f"❌ 连接失败：{result['error']}")
        else:
            print("✅ API 连接成功！")
            print(f"📊 返回数据：{len(result.get('data', {}).get('items', []))} 条记录")
    
    elif command == "daily":
        if len(sys.argv) < 3:
            print("用法：python3 tushare_api.py daily <ts_code> [start_date] [end_date]")
            print("示例：python3 tushare_api.py daily 000001.SZ 20240101 20240131")
            sys.exit(1)
        
        ts_code = sys.argv[2]
        start_date = sys.argv[3] if len(sys.argv) > 3 else None
        end_date = sys.argv[4] if len(sys.argv) > 4 else None
        
        print(f"📈 获取 {ts_code} 行情数据...\n")
        result = get_daily(ts_code, start_date, end_date)
        print(format_daily_output(result))
        
        # Also output JSON for programmatic use
        print("\n---JSON---")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("用法：python3 tushare_api.py info <ts_code>")
            sys.exit(1)
        
        ts_code = sys.argv[2]
        print(f"📋 获取 {ts_code} 基本信息...\n")
        result = get_stock_info(ts_code)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "trade_cal":
        print("📅 获取交易日历...\n")
        exchange = sys.argv[2] if len(sys.argv) > 2 else "SSE"
        result = get_trade_cal(exchange)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "limit":
        trade_date = sys.argv[2] if len(sys.argv) > 2 else None
        print("📊 获取涨跌停统计...\n")
        result = get_limit_list(trade_date)
        if "error" in result:
            print(f"❌ 错误：{result['error']}")
        else:
            formatted, stats = format_limit_output(result, trade_date or datetime.now().strftime("%Y%m%d"))
            print(formatted)
            print("\n---JSON---")
            print(json.dumps({"stats": stats, "raw": result}, ensure_ascii=False, indent=2))
    
    else:
        print(f"❌ 未知命令：{command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
