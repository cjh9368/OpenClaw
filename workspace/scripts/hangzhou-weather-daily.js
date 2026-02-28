#!/usr/bin/env node
/**
 * 杭州每日天气简报 - Telegram 推送版
 * 每天早上 7:10 推送
 * 用法：node hangzhou-weather-daily.js
 */

const https = require('https');

const CITY = '杭州';
const LAT = 30.2741;
const LON = 120.1551;

// WMO weather codes
const WEATHER_CODES = {
  0: { desc: '晴朗', icon: '☀️' },
  1: { desc: '主要晴朗', icon: '🌤️' },
  2: { desc: '部分多云', icon: '⛅' },
  3: { desc: '多云', icon: '☁️' },
  45: { desc: '雾', icon: '🌫️' },
  48: { desc: '雾凇', icon: '🌫️' },
  51: { desc: '毛毛雨', icon: '🌧️' },
  53: { desc: '毛毛雨', icon: '🌧️' },
  55: { desc: '毛毛雨', icon: '🌧️' },
  61: { desc: '小雨', icon: '🌧️' },
  63: { desc: '中雨', icon: '🌧️' },
  65: { desc: '大雨', icon: '🌧️' },
  71: { desc: '小雪', icon: '🌨️' },
  73: { desc: '中雪', icon: '🌨️' },
  75: { desc: '大雪', icon: '🌨️' },
  77: { desc: '雪粒', icon: '🌨️' },
  80: { desc: '阵雨', icon: '🌦️' },
  81: { desc: '阵雨', icon: '🌦️' },
  82: { desc: '强阵雨', icon: '🌦️' },
  95: { desc: '雷雨', icon: '⛈️' },
  96: { desc: '雷雨伴冰雹', icon: '⛈️' },
  99: { desc: '强雷雨伴冰雹', icon: '⛈️' }
};

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : require('http');
    protocol.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('JSON parse error: ' + e.message));
        }
      });
    }).on('error', reject);
  });
}

function getAQIDescription(aqi) {
  if (aqi <= 50) return { level: '优秀', color: '🟢', advice: '空气质量很好' };
  if (aqi <= 100) return { level: '良好', color: '🟡', advice: '空气质量可接受' };
  if (aqi <= 150) return { level: '轻度污染', color: '🟠', advice: '敏感人群减少外出' };
  if (aqi <= 200) return { level: '中度污染', color: '🔴', advice: '减少户外活动' };
  if (aqi <= 300) return { level: '重度污染', color: '🟣', advice: '避免户外活动' };
  return { level: '严重污染', color: '⚫', advice: '避免一切户外活动' };
}

function getClothingRecommendation(tempC, weatherCode, windSpeed) {
  let top = '', bottom = '', note = '';
  
  if (tempC >= 30) {
    top = '短袖 T 恤'; bottom = '短裤/薄长裤'; note = '天气炎热，注意防晒补水';
  } else if (tempC >= 25) {
    top = '短袖 T 恤'; bottom = '长裤'; note = '温暖舒适';
  } else if (tempC >= 20) {
    top = '长袖衬衫/薄卫衣'; bottom = '牛仔裤/休闲裤'; note = '春秋季节，早晚稍凉';
  } else if (tempC >= 15) {
    top = '卫衣/毛衣'; bottom = '牛仔裤'; note = '天气转凉，建议多层穿搭';
  } else if (tempC >= 10) {
    top = '厚毛衣/抓绒衣'; bottom = '厚裤子'; note = '较冷，注意保暖';
  } else if (tempC >= 5) {
    top = '保暖内衣 + 毛衣'; bottom = '厚裤子 + 秋裤'; note = '寒冷，全副武装';
  } else {
    top = '保暖内衣 + 厚毛衣'; bottom = '厚裤子 + 秋裤'; note = '非常寒冷，注意防冻';
  }
  
  const weather = WEATHER_CODES[weatherCode] || { desc: '未知', icon: '❓' };
  if ([51, 53, 55, 61, 63, 65, 80, 81, 82].includes(weatherCode)) {
    note = '有雨，记得带伞 ☔';
  }
  
  return { top, bottom, note, weather };
}

function formatDate(date) {
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const weekday = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][date.getDay()];
  return `${month}月${day}日 ${weekday}`;
}

async function main() {
  try {
    const [weatherData, airData] = await Promise.all([
      getWeather(LAT, LON),
      getAirQuality(LAT, LON).catch(() => null)
    ]);
    
    const current = weatherData.current;
    const daily = weatherData.daily;
    
    const tempC = Math.round(current.temperature_2m);
    const tempMax = Math.round(daily.temperature_2m_max[0]);
    const tempMin = Math.round(daily.temperature_2m_min[0]);
    const weatherCode = current.weather_code;
    const clothing = getClothingRecommendation(tempC, weatherCode, current.wind_speed_10m);
    
    let aqiInfo = { level: '未知', color: '⚪', advice: '数据暂缺' };
    let aqi = '-';
    
    if (airData && airData.current) {
      aqi = airData.current.us_aqi;
      aqiInfo = getAQIDescription(aqi);
    }
    
    const today = new Date();
    const dateStr = formatDate(today);
    
    // 生成简洁报告
    const report = `☀️ 早安！杭州天气简报

📅 ${dateStr}

🌡️ 温度：${tempC}°C (${tempMin}~${tempMax}°C)
${clothing.weather.icon} 天气：${clothing.weather.desc}

🌫️ AQI: ${aqi} ${aqiInfo.color} ${aqiInfo.level}
${aqiInfo.advice}

👕 穿衣：${clothing.top} + ${clothing.bottom}
💡 ${clothing.note}

祝你今天好心情！✨`;

    console.log(report);
    
    // 输出 JSON 供调用方使用
    console.log('\n---JSON---');
    console.log(JSON.stringify({
      report: report,
      temp: tempC,
      aqi: aqi,
      condition: clothing.weather.desc
    }));
    
  } catch (error) {
    console.error('❌ 获取天气失败:', error.message);
    process.exit(1);
  }
}

async function getWeather(lat, lon) {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min&timezone=auto`;
  return await httpGet(url);
}

async function getAirQuality(lat, lon) {
  const url = `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${lat}&longitude=${lon}&current=us_aqi&timezone=auto`;
  return await httpGet(url);
}

main();
