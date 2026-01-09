'use client';

import { useState, useEffect } from 'react';
import { Power, Lightbulb, Plug } from 'lucide-react';
import { energyApi } from '@/services/api';
import { RelayStates } from '@/types';

const DEVICE_MAP = [
    { id: 'relay1', name: 'Bulb 1', icon: Lightbulb },
    { id: 'relay2', name: 'Bulb 2', icon: Lightbulb },
    { id: 'relay3', name: 'Socket 1', icon: Plug },
    { id: 'relay4', name: 'Socket 2', icon: Plug },
];

export default function DeviceControl() {
    const [states, setStates] = useState<RelayStates>({});
    const [loading, setLoading] = useState(true);
    const [toggling, setToggling] = useState<string | null>(null);

    useEffect(() => {
        const fetchStates = async () => {
            try {
                const data = await energyApi.getRelayStates();
                setStates(data);
            } catch (error) {
                console.error('Error fetching relay states:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchStates();
        const interval = setInterval(fetchStates, 5000); // Poll every 5 seconds for hardware changes
        return () => clearInterval(interval);
    }, []);

    const handleToggle = async (relayId: string, currentState: boolean) => {
        setToggling(relayId);
        try {
            await energyApi.updateRelayState(relayId, !currentState);
            setStates((prev) => ({ ...prev, [relayId]: !currentState }));
        } catch (error) {
            console.error('Error toggling device:', error);
        } finally {
            setToggling(null);
        }
    };

    if (loading && Object.keys(states).length === 0) {
        return (
            <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm animate-pulse">
                <div className="h-6 w-32 bg-slate-200 rounded mb-6"></div>
                <div className="grid grid-cols-2 gap-4">
                    {[1, 2, 3, 4].map((i) => (
                        <div key={i} className="h-20 bg-slate-100 rounded-xl"></div>
                    ))}
                </div>
            </div>
        );
    }

    return (
        <section className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                    <Power size={20} className="text-blue-600" />
                    Device Control
                </h2>
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 bg-slate-50 px-2 py-1 rounded-md border border-slate-100">
                    Real-time Firebase Sync
                </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {DEVICE_MAP.map((device) => {
                    const isActive = states[device.id] || false;
                    const Icon = device.icon;
                    const isProcessing = toggling === device.id;

                    return (
                        <button
                            key={device.id}
                            onClick={() => handleToggle(device.id, isActive)}
                            disabled={isProcessing}
                            className={`relative flex flex-col items-center justify-center p-4 rounded-xl transition-all duration-300 border-2 ${isActive
                                    ? 'bg-blue-50 border-blue-200 text-blue-700 shadow-sm'
                                    : 'bg-slate-50 border-transparent text-slate-500 hover:bg-slate-100'
                                } ${isProcessing ? 'opacity-70 cursor-wait' : ''}`}
                        >
                            <div
                                className={`p-3 rounded-full mb-2 ${isActive ? 'bg-blue-500 text-white shadow-lg shadow-blue-200' : 'bg-slate-200 text-slate-500'
                                    }`}
                            >
                                <Icon size={24} />
                            </div>
                            <span className="font-bold text-sm">{device.name}</span>
                            <span className={`text-[10px] font-bold uppercase mt-1 ${isActive ? 'text-blue-600' : 'text-slate-400'}`}>
                                {isActive ? 'ON' : 'OFF'}
                            </span>

                            {isProcessing && (
                                <div className="absolute inset-0 flex items-center justify-center bg-white/40 rounded-xl">
                                    <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                                </div>
                            )}
                        </button>
                    );
                })}
            </div>
        </section>
    );
}
