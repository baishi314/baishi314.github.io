// components/WeatherWidget.tsx
"use client";

import { useState, useEffect } from 'react';
import { Cloud, Sun, CloudRain, Snowflake, CloudLightning, Loader2, Wind } from 'lucide-react';

export default function WeatherWidget() {
  const [weather, setWeather] = useState<{ city: string; temp: number; text: string; icon: string; isMock: boolean } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWeather = async () => {
      // 静态站点：用免 Key 的开放接口 wttr.in（支持 CORS）
      const CITY = 'Qinhuangdao';
      try {
        const res = await fetch(`https://wttr.in/${CITY}?format=j1`);
        if (!res.ok) throw new Error('weather http ' + res.status);
        const data = await res.json();
        const cur = data.current_condition?.[0];
        if (!cur) throw new Error('no current_condition');

        // wttr.in weatherCode -> 和风图标码（保持原组件的映射逻辑）
        const codeMap: Record<string, string> = {
          '113': '100', '116': '101', '119': '104', '122': '104',
          '143': '501', '248': '501', '260': '501',
          '176': '305', '263': '305', '266': '305', '293': '305', '296': '305',
          '299': '306', '302': '306', '305': '307', '308': '308', '353': '305',
          '356': '306', '359': '308',
          '179': '400', '182': '400', '185': '400', '227': '407', '230': '407',
          '200': '302', '386': '302', '389': '302', '392': '302', '395': '302',
        };
        const wcode = cur.weatherCode || '113';

        setWeather({
          city: '\u79e6\u7687\u5c9b\u5e02',
          temp: parseInt(cur.temp_C, 10),
          text: cur.lang_zh?.[0]?.value || cur.weatherDesc?.[0]?.value || '\u672a\u77e5',
          icon: codeMap[wcode] || '104',
          isMock: false,
        });
      } catch (err) {
        setWeather({ city: '\u79e6\u7687\u5c9b\u5e02', temp: 22, text: '\u6c14\u5019\u6a21\u62df', icon: '101', isMock: true });
      } finally {
        setLoading(false);
      }
    };

    fetchWeather();
  }, []);

  // 图标映射逻辑保持不变...
  const getWeatherIcon = (iconCode: string) => {
    const code = parseInt(iconCode);
    if (code === 100) return <Sun className="text-amber-400" size={38} />;
    if (code >= 101 && code <= 104) return <Cloud className="text-slate-300" size={38} />;
    if (code >= 300 && code <= 399) return <CloudRain className="text-blue-400" size={38} />;
    if (code >= 400 && code <= 499) return <Snowflake className="text-indigo-200" size={38} />;
    if (code >= 150 && code <= 153) return <Sun className="text-orange-200" size={38} />; // 夜间晴/多云
    return <Cloud className="text-slate-400" size={38} />;
  };

  return (
    <div className="w-full h-full rounded-3xl bg-white/40 dark:bg-slate-800/50 backdrop-blur-md border border-white/40 dark:border-white/10 shadow-xl p-6 flex flex-col justify-center transition-all duration-700 hover:scale-[1.02] group relative overflow-hidden">
      <div className={`absolute -right-6 -top-6 w-32 h-32 blur-3xl rounded-full transition-colors duration-700 ${weather?.isMock ? 'bg-amber-500/20 group-hover:bg-amber-500/40' : 'bg-indigo-500/20 group-hover:bg-indigo-500/40'}`}></div>
      {loading ? (
         <div className="flex flex-col items-center gap-3 text-slate-500 w-full justify-center relative z-10">
           <Loader2 className="animate-spin text-indigo-400" size={28} />
           <span className="text-[10px] font-black tracking-widest uppercase">同步 V7 气象云...</span>
         </div>
      ) : weather && (
        <div className="flex items-center justify-between relative z-10 w-full">
          <div className="flex flex-col flex-1 pr-2">
            <span className={`text-[10px] font-black uppercase tracking-widest mb-1 ${weather.isMock ? 'text-amber-500' : 'text-indigo-500 dark:text-indigo-400'}`}>
              {weather.isMock ? 'SIMULATED V7' : 'QINHUANGDAO'}
            </span>
            <span className="text-base font-bold text-slate-800 dark:text-white line-clamp-1">{weather.city}</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-3xl font-black text-slate-900 dark:text-slate-100 tracking-tighter">{weather.temp}°</span>
              <span className="text-xs font-bold text-slate-500">{weather.text}</span>
            </div>
          </div>
          <div className="relative z-10 group-hover:scale-110 transition-transform duration-500 drop-shadow-md">
            {getWeatherIcon(weather.icon)}
          </div>
        </div>
      )}
    </div>
  );
}