import { Zap, Activity, AlertCircle } from 'lucide-react';
import Link from 'next/link';

interface DeviceCardProps {
    name: string;
    status: 'normal' | 'warning' | 'anomaly';
    currentPower: number;
    energyToday: number;
    lastUpdate: string;
}

export default function DeviceCard({ name, status, currentPower, energyToday, lastUpdate }: DeviceCardProps) {
    const statusColors = {
        normal: 'text-green-500 bg-green-50',
        warning: 'text-yellow-500 bg-yellow-50',
        anomaly: 'text-red-500 bg-red-50',
    };

    const statusLabels = {
        normal: 'Normal Operations',
        warning: 'High Usage',
        anomaly: 'Anomaly Detected',
    };

    return (
        <Link href={`/devices/${name}`} className="group bg-white rounded-3xl p-5 md:p-6 shadow-sm border border-slate-100 hover:border-blue-200 hover:shadow-lg transition-all duration-300">
            <div className="flex items-center justify-between mb-4 md:mb-6">
                <h3 className="text-lg font-bold text-slate-900 capitalize">{name.replace('_', ' ')}</h3>
                <span className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold ${statusColors[status]}`}>
                    {status === 'anomaly' ? <AlertCircle size={14} /> : <Activity size={14} />}
                    {statusLabels[status]}
                </span>
            </div>

            <div className="grid grid-cols-2 gap-3 md:gap-4 mb-4 md:mb-6">

                <div className="bg-slate-50 rounded-2xl p-4">
                    <p className="text-xs text-slate-500 font-medium mb-1 flex items-center gap-1">
                        <Zap size={12} /> Live Power
                    </p>
                    <div className="flex items-baseline gap-1">
                        <span className="text-lg font-bold text-slate-900">{currentPower.toFixed(1)}</span>
                        <span className="text-xs font-semibold text-slate-400">W</span>
                    </div>
                </div>
                <div className="bg-slate-50 rounded-2xl p-4">
                    <p className="text-xs text-slate-500 font-medium mb-1">Today</p>
                    <div className="flex items-baseline gap-1">
                        <span className="text-lg font-bold text-slate-900">{energyToday.toFixed(3)}</span>
                        <span className="text-xs font-semibold text-slate-400">kWh</span>
                    </div>
                </div>
            </div>

            <div className="flex items-center justify-between text-xs text-slate-400">
                <span>Updated {lastUpdate}</span>
                <span className="group-hover:text-blue-600 font-semibold flex items-center gap-1 transition-colors">
                    View details →
                </span>
            </div>
        </Link>
    );
}
