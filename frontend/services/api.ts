import {
    Reading,
    Device,
    AnomalyResponse,
    DailySummary,
    ForecastResponse,
    RelayStates
} from '../types';

const getApiBaseUrl = () => {
    let url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    // If it looks like a Render service name without a domain (no dots)
    if (!url.includes('.') && !url.includes('localhost')) {
        url = `${url}.onrender.com`;
    }

    if (url.startsWith('http')) return url;
    return `https://${url}`;
};

const API_BASE_URL = getApiBaseUrl();
console.log('🌐 API_BASE_URL initialized as:', API_BASE_URL);

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    console.log(`🔍 Fetching: ${url}`);

    const response = await fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options?.headers,
        },
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || response.statusText);
    }

    return response.json();
}

export const energyApi = {
    // Readings
    getLatestReadings: () => fetchApi<Reading[]>('/readings/latest'),
    getDeviceReadings: (device: string, limit = 100) =>
        fetchApi<Reading[]>(`/readings/device/${device}?limit=${limit}`),

    // Analytics
    getDailySummary: (date: string) =>
        fetchApi<DailySummary>(`/analytics/daily-summary?day=${date}`),
    getHighestConsumer: (date: string) =>
        fetchApi<any>(`/analytics/highest-consumer?day=${date}`),

    // Anomalies
    getAnomalies: (device: string) =>
        fetchApi<AnomalyResponse>(`/anomalies/${device}`),
    setDeviceThreshold: (device: string, threshold: number) =>
        fetchApi<Device>(`/anomalies/devices/${device}/threshold`, {
            method: 'POST',
            body: JSON.stringify({ threshold }),
        }),
    getDeviceThreshold: (device: string) =>
        fetchApi<Device>(`/anomalies/devices/${device}/threshold`),
    getAllDevices: () => fetchApi<Device[]>('/anomalies/devices'),

    // Forecast

    getForecast: (days = 7) =>
        fetchApi<ForecastResponse>(`/forecast/?days=${days}`, { method: 'POST' }),

    // Chatbot
    queryChat: (question: string, sessionId: string) =>
        fetchApi<{ answer: string }>('/chatbot/query', {
            method: 'POST',
            body: JSON.stringify({ question, session_id: sessionId }),
        }),

    // Device Control
    getRelayStates: () => fetchApi<RelayStates>('/devices/'),
    updateRelayState: (relayId: string, state: boolean) =>
        fetchApi<{ relay_id: string; state: boolean }>(`/devices/${relayId}`, {
            method: 'PATCH',
            body: JSON.stringify({ state }),
        }),
};
