export interface Reading {
    id: number;
    device: string;
    timestamp: string;
    current: number;
    voltage: number;
}

export interface Device {
    id: string; // device name
    threshold: number;
}

export interface AnomalyResponse {
    device_id: string;
    threshold: number;
    anomalies: Reading[];
}

export interface DeviceStats {
    device: string;
    total_energy: number;
    avg_voltage: number;
    avg_current: number;
}

export interface DailySummary {
    date: string;
    total_energy: number;
    device_breakdown: DeviceStats[];
}

export interface ForecastItem {
    date: string;
    predicted_energy: number;
}

export interface ForecastResponse {
    forecast: ForecastItem[];
}

export interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
}
