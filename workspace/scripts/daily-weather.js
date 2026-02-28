#!/usr/bin/env node
/**
 * Daily Weather Report Script
 * Uses Open-Meteo API (no API key required)
 * Usage: node daily-weather.js [city] [latitude] [longitude]
 */

const https = require('https');

// Default: Hangzhou coordinates
const DEFAULT_CITY = '杭州';
const DEFAULT_LAT = 30.2741;
const DEFAULT_LON = 120.1551;

const CITY = process.argv[2] || DEFAULT_CITY;
const LAT = parseFloat(process.argv[3]) || DEFAULT_LAT;
const LON = parseFloat(process.argv[4]) || DEFAULT_LON;

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

// HTTP GET request helper
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

// Get weather data from Open-Meteo
async function getWeather(lat, lon) {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=auto`;
  return await httpGet(url);
}

// Get air quality from Open-Meteo
async function getAirQuality(lat, lon) {
  const url = `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${lat}&longitude=${lon}&current=us_aqi,pm2_5,pm10&timezone=auto`;
  return await httpGet(url);
}

// Get clothing recommendation
function getClothingRecommendation(tempC, weatherCode, windSpeed) {
  const feelsLike = tempC - (windSpeed * 0.1);
  
  let clothing = { top: '', bottom: '', accessories: [], note: '' };
  
  // Temperature-based
  if (tempC >= 30) {
    clothing.top = '短袖 T 恤/背心';
    clothing.bottom = '短裤/薄长裤';
    clothing.accessories = ['太阳镜', '帽子'];
    clothing.note = '天气炎热，注意防晒和补水';
  } else if (tempC >= 25) {
    clothing.top = '短袖 T 恤/薄衬衫';
    clothing.bottom = '长裤/薄牛仔裤';
    clothing.accessories = ['太阳镜'];
    clothing.note = '温暖舒适，适合轻薄衣物';
  } else if (tempC >= 20) {
    clothing.top = '长袖衬衫/薄卫衣';
    clothing.bottom = '牛仔裤/休闲裤';
    clothing.accessories = ['薄外套'];
    clothing.note = '春秋季节，早晚可能稍凉';
  } else if (tempC >= 15) {
    clothing.top = '卫衣/毛衣';
    clothing.bottom = '牛仔裤/厚休闲裤';
    clothing.accessories = ['夹克/风衣'];
    clothing.note = '天气转凉，建议多层穿搭';
  } else if (tempC >= 10) {
    clothing.top = '厚毛衣/抓绒衣';
    clothing.bottom = '厚牛仔裤/休闲裤';
    clothing.accessories = ['厚外套', '围巾'];
    clothing.note = '较冷，注意保暖';
  } else if (tempC >= 5) {
    clothing.top = '保暖内衣 + 毛衣';
    clothing.bottom = '厚裤子/秋裤';
    clothing.accessories = ['羽绒服/厚大衣', '手套', '帽子'];
    clothing.note = '寒冷，全副武装保暖';
  } else {
    clothing.top = '保暖内衣 + 厚毛衣';
    clothing.bottom = '厚裤子 + 秋裤';
    clothing.accessories = ['厚羽绒服', '围巾', '手套', '保暖帽'];
    clothing.note = '非常寒冷，注意防冻';
  }
  
  // Weather adjustments
  const weather = WEATHER_CODES[weatherCode] || { desc: '未知', icon: '❓' };
  
  if ([51, 53, 55, 61, 63, 65, 80, 81, 82].includes(weatherCode)) {
    clothing.accessories.push('☔ 雨伞/雨衣');
    clothing.note = '有雨，记得带伞';
  }
  
  if ([71, 73, 75, 77].includes(weatherCode)) {
    clothing.accessories.push('防滑鞋');
    clothing.note = '下雪路滑，注意防滑';
  }
  
  if (windSpeed > 20) {
    clothing.accessories.push('防风外套');
    clothing.note += '，风大注意防风';
  }
  
  return { ...clothing, weather };
}

// Get AQI description
function getAQIDescription(aqi) {
  if (aqi <= 50) return { level: '优秀', color: '🟢', advice: '空气质量很好，适合户外活动' };
  if (aqi <= 100) return { level: '良好', color: '🟡', advice: '空气质量可接受，敏感人群减少外出' };
  if (aqi <= 150) return { level: '轻度污染', color: '🟠', advice: '敏感人群减少户外活动' };
  if (aqi <= 200) return { level: '中度污染', color: '🔴', advice: '所有人减少户外活动，外出戴口罩' };
  if (aqi <= 300) return { level: '重度污染', color: '🟣', advice: '避免户外活动，必须外出时戴 N95 口罩' };
  return { level: '严重污染', color: '⚫', advice: '避免一切户外活动，关闭门窗' };
}

// Format date
function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const weekday = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][date.getDay()];
  return `${year}年${month}月${day}日 ${weekday}`;
}

// Wind direction
function getWindDirection(degrees) {
  const dirs = ['北', '东北', '东', '东南', '南', '西南', '西', '西北'];
  return dirs[Math.round(degrees / 45) % 8];
}

// Main function
async function main() {
  try {
    console.log(`📍 获取 ${CITY} 天气信息...\n`);
    
    // Get weather and air quality in parallel
    const [weatherData, airData] = await Promise.all([
      getWeather(LAT, LON),
      getAirQuality(LAT, LON).catch(() => null) // Air quality is optional
    ]);
    
    const current = weatherData.current;
    const daily = weatherData.daily;
    
    const tempC = Math.round(current.temperature_2m);
    const tempMax = Math.round(daily.temperature_2m_max[0]);
    const tempMin = Math.round(daily.temperature_2m_min[0]);
    const humidity = current.relative_humidity_2m;
    const weatherCode = current.weather_code;
    const windSpeed = Math.round(current.wind_speed_10m);
    const windDir = getWindDirection(current.wind_direction_10m);
    
    const weather = WEATHER_CODES[weatherCode] || { desc: '未知', icon: '❓' };
    
    // Air quality
    let aqiInfo = { level: '未知', color: '⚪', advice: '数据暂缺' };
    let aqi = '-', pm25 = '-', pm10 = '-';
    
    if (airData && airData.current) {
      aqi = airData.current.us_aqi;
      pm25 = airData.current.pm2_5;
      pm10 = airData.current.pm10;
      aqiInfo = getAQIDescription(aqi);
    }
    
    // Clothing recommendation
    const clothing = getClothingRecommendation(tempC, weatherCode, windSpeed);
    
    // Date
    const today = new Date();
    const dateStr = formatDate(today);
    
    // Generate report
    const report = `
╔═══════════════════════════════════════════════════════════╗
║                    🌤️ 每日天气提醒                        ║
╠═══════════════════════════════════════════════════════════╣
║  📅 ${dateStr.padStart(39, ' ')}║
║  📍 ${CITY.padStart(42, ' ')}║
╠═══════════════════════════════════════════════════════════╣
║  🌡️  当前：${tempC}°C  最高：${tempMax}°C  最低：${tempMin}°C${' '.repeat(16 - tempC.toString().length - tempMax.toString().length - tempMin.toString().length)}║
║  ${weather.icon}  天气：${weather.desc.padStart(37, ' ')}║
║  💧  湿度：${humidity}%${' '.repeat(37 - humidity.toString().length)}║
║  💨  风力：${windDir}风 ${windSpeed}km/h${' '.repeat(28 - windDir.length - windSpeed.toString().length)}║
╠═══════════════════════════════════════════════════════════╣
║  🌫️  空气质量指数 (AQI): ${aqi}${aqi !== '-' ? ' ' + aqiInfo.color : ''}${' '.repeat(19 - aqi.toString().length)}║
║  📊  等级：${aqiInfo.level.padStart(36, ' ')}║
║  🔬  PM2.5: ${pm25}${pm25 !== '-' ? ' μg/m³' : ''}${' '.repeat(28 - pm25.toString().length)}║
║  💡  ${aqiInfo.advice.substring(0, 36).padEnd(36, ' ')}║
╠═══════════════════════════════════════════════════════════╣
║  👕 上衣：${clothing.top.padStart(37, ' ')}║
║  👖 裤子：${clothing.bottom.padStart(36, ' ')}║
║  🎒 配件：${clothing.accessories.join(' + ').padStart(36, ' ')}║
║  💬 ${clothing.note.padEnd(40, ' ')}║
╚═══════════════════════════════════════════════════════════╝
`;

    console.log(report);
    
    // Output JSON
    console.log('\n---JSON---');
    console.log(JSON.stringify({
      date: dateStr,
      city: CITY,
      weather: {
        temp_current: tempC,
        temp_max: tempMax,
        temp_min: tempMin,
        condition: weather.desc,
        icon: weather.icon,
        humidity: humidity,
        wind: `${windDir}风 ${windSpeed}km/h`
      },
      air_quality: {
        aqi: aqi,
        level: aqiInfo.level,
        pm25: pm25,
        advice: aqiInfo.advice
      },
      clothing: {
        top: clothing.top,
        bottom: clothing.bottom,
        accessories: clothing.accessories,
        note: clothing.note
      }
    }, null, 2));
    
  } catch (error) {
    console.error('❌ 获取天气失败:', error.message);
    process.exit(1);
  }
}

main();
