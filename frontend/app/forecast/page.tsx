'use client';

import { useEffect, useState } from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    AreaChart,
    Area
} from 'recharts';
import { TrendingUp, Calendar, Info, Lightbulb } from 'lucide-react';
import { energyApi } from '@/services/api';
import { ForecastItem } from '@/types';

export default function ForecastPage() {
    const [duration, setDuration] = useState(7);
    const [forecastData, setForecastData] = useState<ForecastItem[]>([]);
    const [outlook, setOutlook] = useState("");
    const [tip, setTip] = useState("");
    const [loading, setLoading] = useState(true);

    const fetchForecast = async (days: number) => {
        setLoading(true);
        try {
            const data = await energyApi.getForecast(days);
            setForecastData(data.forecast);
            setOutlook(data.outlook);
            setTip(data.tip);
        } catch (error) {
            console.error('Error fetching forecast:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchForecast(duration);
    }, [duration]);

    const durations = [3, 7, 14, 30];

    return (
        <div className="space-y-8 pb-12">
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Consumption Forecasting</h1>
                    <p className="text-slate-500 font-medium">AI-powered predictions for your future energy usage.</p>
                </div>

                <div className="flex bg-white p-1.5 rounded-2xl shadow-sm border border-slate-100 w-fit">
                    {durations.map((d) => (
                        <button
                            key={d}
                            onClick={() => setDuration(d)}
                            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${duration === d
                                ? 'bg-blue-600 text-white shadow-lg shadow-blue-200'
                                : 'text-slate-500 hover:text-slate-800'
                                }`}
                        >
                            {d} Days
                        </button>
                    ))}
                </div>
            </header>


            {/* Forecast Chart Card */}
            <div className="bg-white rounded-[1.5rem] md:rounded-[2rem] p-5 md:p-8 border border-slate-100 shadow-sm">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-6 md:mb-8 gap-4">
                    <div>
                        <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                            <TrendingUp size={20} className="text-blue-600" /> {duration}-Day Prediction
                        </h3>
                        <p className="text-sm text-slate-500 font-medium">Estimated energy usage in kWh</p>
                    </div>
                    <div className="bg-slate-50 px-4 py-2 rounded-xl flex items-center gap-2 text-slate-600 text-sm font-bold w-fit">
                        <Calendar size={16} /> Next {duration} Days
                    </div>
                </div>

                <div className="h-[300px] md:h-[400px] w-full">
                    {loading ? (
                        <div className="h-full w-full flex items-center justify-center">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                        </div>
                    ) : forecastData.length === 0 ? (
                        <div className="h-full w-full flex flex-col items-center justify-center text-slate-400 gap-3">
                            <Info size={40} />
                            <p className="font-medium text-black">Insufficient data for a reliable forecast yet.</p>
                            <p className="text-sm text-black">Keep the system running for a few more days!</p>
                        </div>
                    ) : (
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={forecastData}>
                                <defs>
                                    <linearGradient id="colorUsage" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                                <XAxis
                                    dataKey="date"
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#64748b', fontSize: 12, fontWeight: 500 }}
                                    dy={10}
                                />
                                <YAxis
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#64748b', fontSize: 12, fontWeight: 500 }}
                                />
                                <Tooltip
                                    contentStyle={{
                                        borderRadius: '16px',
                                        border: 'none',
                                        boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
                                        padding: '12px'
                                    }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="predicted_energy"
                                    stroke="#3b82f6"
                                    strokeWidth={3}
                                    fillOpacity={1}
                                    fill="url(#colorUsage)"
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    )}
                </div>
            </div>

            {/* Insights Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
                <div className="bg-blue-50/50 rounded-[1.5rem] md:rounded-3xl p-5 md:p-6 border border-blue-100 min-h-[120px]">
                    <h4 className="font-bold text-blue-900 flex items-center gap-2 mb-2 md:mb-3">
                        <Lightbulb size={18} /> Tomorrow's Outlook
                    </h4>
                    {loading ? (
                        <div className="h-4 bg-blue-100 rounded w-3/4 animate-pulse"></div>
                    ) : (
                        <p className="text-blue-800 text-sm leading-relaxed font-medium">
                            {outlook || "No specific outlook available yet."}
                        </p>
                    )}
                </div>
                <div className="bg-purple-50/50 rounded-[1.5rem] md:rounded-3xl p-5 md:p-6 border border-purple-100 min-h-[120px]">
                    <h4 className="font-bold text-purple-900 flex items-center gap-2 mb-2 md:mb-3">
                        ✨ Energy Saving Tip
                    </h4>
                    {loading ? (
                        <div className="h-4 bg-purple-100 rounded w-3/4 animate-pulse"></div>
                    ) : (
                        <p className="text-purple-800 text-sm leading-relaxed font-medium">
                            {tip || "No specific saving tips available based on current data."}
                        </p>
                    )}
                </div>
            </div>

            {/* Learning Note */}
            <div className="bg-white rounded-[1.5rem] md:rounded-[2rem] p-5 md:p-8 border border-slate-100 shadow-sm">
                <h3 className="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
                    🎓 How does Forecasting work?
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="space-y-2">
                        <div className="w-10 h-10 bg-blue-600 text-white rounded-xl flex items-center justify-center font-bold">1</div>
                        <h5 className="font-bold text-slate-900">Data Collection</h5>
                        <p className="text-sm text-slate-500 leading-relaxed font-medium text-black">
                            First, our sensors record your actual energy usage every day to build a historical dataset.
                        </p>
                    </div>
                    <div className="space-y-2">
                        <div className="w-10 h-10 bg-blue-600 text-white rounded-xl flex items-center justify-center font-bold">2</div>
                        <h5 className="font-bold text-slate-900">Pattern Finder</h5>
                        <p className="text-sm text-slate-500 leading-relaxed font-medium text-black">
                            The AI model looks for &quot;seasonal&quot; patterns (like higher usage on weekends or at night).
                        </p>
                    </div>
                    <div className="space-y-2">
                        <div className="w-10 h-10 bg-blue-600 text-white rounded-xl flex items-center justify-center font-bold">3</div>
                        <h5 className="font-bold text-slate-900">Projecting Forward</h5>
                        <p className="text-sm text-slate-500 leading-relaxed font-medium text-black">
                            Finally, the model extends these patterns into the future to create the forecast you see above!
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
