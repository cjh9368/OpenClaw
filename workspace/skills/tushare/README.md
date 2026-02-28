# Tushare 股票数据 API

中国 A 股股票数据接口，提供实时行情、历史数据、财务数据等。

## 快速开始

```bash
# 测试 API 连接
python3 /home/admin/.openclaw/workspace/skills/tushare/tushare_api.py test

# 获取股票行情（默认最近 30 天）
python3 /home/admin/.openclaw/workspace/skills/tushare/tushare_api.py daily 000001.SZ

# 获取指定日期范围
python3 /home/admin/.openclaw/workspace/skills/tushare/tushare_api.py daily 000001.SZ 20240101 20240131

# 获取股票基本信息
python3 /home/admin/.openclaw/workspace/skills/tushare/tushare_api.py info 000001.SZ
```

## API 配置

- **Token**: `828abf5aa2217e5f0d0ab35b0e57f0441149775885cdd7ec7588bac36c04`
- **API URL**: `http://lianghua.nanyangqiankun.top`
- **版本**: tushare 1.4.24 兼容

## 常用命令

### 1. 获取日线行情

```bash
python3 tushare_api.py daily <ts_code> [start_date] [end_date]
```

**参数**:
- `ts_code`: 股票代码，格式 `XXXXXX.SZ` 或 `XXXXXX.SH`
- `start_date`: 开始日期，格式 `YYYYMMDD`（可选，默认 30 天前）
- `end_date`: 结束日期，格式 `YYYYMMDD`（可选，默认今天）

**示例**:
```bash
# 平安银行最近 30 天
python3 tushare_api.py daily 000001.SZ

# 指定日期范围
python3 tushare_api.py daily 600519.SH 20240101 20240131
```

### 2. 获取股票基本信息

```bash
python3 tushare_api.py info <ts_code>
```

### 3. 获取交易日历

```bash
python3 tushare_api.py trade_cal [exchange]
```

**exchange**: `SSE` (上交所) 或 `SZSE` (深交所)

## 股票代码示例

| 股票 | 代码 |
|------|------|
| 平安银行 | 000001.SZ |
| 贵州茅台 | 600519.SH |
| 上证指数 | 000001.SH |
| 深证成指 | 399001.SZ |
| 创业板指 | 399006.SZ |

## 返回数据字段

### daily 日线数据

| 字段 | 说明 |
|------|------|
| ts_code | 股票代码 |
| trade_date | 交易日期 |
| open | 开盘价 |
| high | 最高价 |
| low | 最低价 |
| close | 收盘价 |
| pre_close | 昨收价 |
| change | 涨跌额 |
| pct_chg | 涨跌幅% |
| vol | 成交量（手） |
| amount | 成交额（千元） |

## Python 原生用法

```python
import tushare as ts

token = "828abf5aa2217e5f0d0ab35b0e57f0441149775885cdd7ec7588bac36c04"
pro = ts.pro_api(token)
pro._DataApi__token = token
pro._DataApi__http_url = 'http://lianghua.nanyangqiankun.top'

# 获取日线数据
df = pro.daily(ts_code='000001.SZ', start_date='20240101', end_date='20240131')
print(df)

# 获取股票基本信息
df = pro.stock_basic(ts_code='000001.SZ')
print(df)
```

## 注意事项

1. **Token 安全**: 不要公开分享你的 API token
2. **请求限制**: 避免频繁请求，建议添加延时
3. **数据延迟**: 实时行情可能有 15 分钟延迟
4. **交易时间**: 非交易时间获取的是最新收盘数据

## 故障排除

**连接失败**:
- 检查 API URL 是否正确
- 检查网络连接
- 确认 token 有效

**无数据返回**:
- 确认股票代码格式正确
- 确认日期范围在交易日内
- 确认股票是否停牌

## 资源

- [Tushare 官方文档](https://tushare.pro/document/2)
- [API 接口大全](https://tushare.pro/document/2?doc_id=27)
