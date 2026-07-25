export interface ActionLogItem {
  timestamp: string;
  node: string;
  status: string;
  message: string;
  details?: Record<string, any>;
}

export interface FlightOption {
  id: string;
  airline: string;
  flight_number: string;
  origin: str;
  destination: string;
  departure_time: string;
  arrival_time: string;
  duration: string;
  price_inr: number;
  is_mock: boolean;
  source_label: string;
}

export interface HotelOption {
  id: string;
  name: string;
  location: string;
  rating: number;
  price_per_night_inr: number;
  total_price_inr: number;
  nights: number;
  amenities: string[];
  image_url?: string;
  is_mock: boolean;
  source_label: string;
}

export interface WeatherForecastDay {
  date: string;
  temp_max: number;
  temp_min: number;
  condition: string;
  rain_prob: number;
}

export interface WeatherInfo {
  city: string;
  forecast: WeatherForecastDay[];
  summary: string;
  is_mock: boolean;
}

export interface TripResponse {
  success: boolean;
  origin: string;
  destination: string;
  start_date: string;
  end_date: string;
  max_budget: number;
  total_cost: number;
  is_within_budget: boolean;
  selected_flight?: FlightOption;
  selected_hotel?: HotelOption;
  weather_info?: WeatherInfo;
  summary: string;
  itinerary: any;
  action_logs: ActionLogItem[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function planTrip(payload: {
  query: string;
  origin?: string;
  destination?: string;
  max_budget?: number;
}): Promise<TripResponse> {
  const response = await fetch(`${API_BASE_URL}/api/plan`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API error (${response.status}): ${errorText}`);
  }

  return response.json();
}
