import { LucideIcon } from 'lucide-react';

interface StatCardProps {
    title: string;
    value: string | number;
    unit?: string;
    icon: LucideIcon;
    trend?: {
        value: number;
        trend_value?: number;
        isUp: boolean;
    };
    color: string;
}

export default function StatCard({ title, value, unit, icon: Icon, trend, color }: StatCardProps) {
    return (
        <div className="bg-white rounded-3xl p-5 md:p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow duration-300">
            <div className="flex items-start justify-between mb-4">
                <div className={`p-3 rounded-2xl ${color} bg-opacity-10`}>
                    <Icon className={color.replace('bg-', 'text-')} size={24} />
                </div>
                {trend && (
                    <div className={`flex items-center gap-1 text-xs font-bold px-2 py-1 rounded-full ${trend.isUp ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'
                        }`}>
                        {trend.isUp ? '↑' : '↓'} {trend.trend_value ?? trend.value}%
                    </div>
                )}
            </div>
            <div>
                <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
                <div className="flex items-baseline gap-1">
                    <h3 className="text-2xl font-bold text-slate-900">{value}</h3>
                    {unit && <span className="text-sm font-semibold text-slate-400">{unit}</span>}
                </div>
            </div>
        </div>
    );
}
