#!/usr/bin/env node
/**
 * Send Daily Weather Report via Feishu
 * This script is called by cron job every morning at 7:10
 */

const { exec } = require('child_process');
const path = require('path');

const CITY = process.argv[2] || '杭州';
const LAT = process.argv[3] || 30.2741;
const LON = process.argv[4] || 120.1551;

const WEATHER_SCRIPT = path.join(__dirname, 'daily-weather.js');

// Execute weather script
exec(`node "${WEATHER_SCRIPT}" "${CITY}" ${LAT} ${LON}`, (error, stdout, stderr) => {
  if (error) {
    console.error(`❌ 执行失败：${error.message}`);
    process.exit(1);
  }
  
  if (stderr) {
    console.error(`stderr: ${stderr}`);
  }
  
  // Parse the output to extract the formatted report
  const jsonStart = stdout.indexOf('---JSON---');
  let reportText = stdout;
  let jsonData = null;
  
  if (jsonStart !== -1) {
    reportText = stdout.substring(0, jsonStart).trim();
    const jsonStr = stdout.substring(jsonStart + 10).trim();
    try {
      jsonData = JSON.parse(jsonStr);
    } catch (e) {
      console.error('JSON 解析失败:', e.message);
    }
  }
  
  console.log('✅ 天气报告生成成功');
  console.log('\n' + reportText);
  
  // Output for cron job
  if (jsonData) {
    console.log('\n📊 摘要:');
    console.log(`${jsonData.city} ${jsonData.weather.icon} ${jsonData.weather.condition}`);
    console.log(`🌡️ ${jsonData.weather.temp_current}°C (${jsonData.weather.temp_min}~${jsonData.weather.temp_max}°C)`);
    console.log(`🌫️ AQI ${jsonData.air_quality.aqi} - ${jsonData.air_quality.level}`);
    console.log(`👕 ${jsonData.clothing.top} + ${jsonData.clothing.bottom}`);
    console.log(`💡 ${jsonData.clothing.note}`);
  }
});
