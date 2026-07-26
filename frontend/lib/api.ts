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
  origin: string;
  destination: string;
  departure_time: string;
  arrival_time: string;
  duration: string;
  price_inr: number;
  is_mock?: boolean;
  source_label?: string;
}

export interface HotelOption {
  id: string;
  name: string;
  location: string;
  rating: number;
  price_per_night_inr: number;
  total_price_inr: number;
  nights?: number;
  amenities?: string[];
  image_url?: string;
  is_mock?: boolean;
  source_label?: string;
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
  is_mock?: boolean;
}

export interface AttractionItem {
  name: string;
  category: string;
  short_description: string;
}

export interface FoodItem {
  name: string;
  cuisine_type: string;
  short_description: string;
}

export interface ActivitiesInfo {
  city_code?: string;
  city_name?: string;
  attractions?: AttractionItem[];
  food_recommendations?: FoodItem[];
}

export interface TripResponse {
  success?: boolean;
  origin: string;
  destination: string;
  start_date: string;
  end_date?: string;
  max_budget?: number;
  budget_inr?: number;
  total_cost: number;
  is_within_budget?: boolean;
  budget_status?: string;
  selected_flight?: FlightOption;
  selected_hotel?: HotelOption;
  weather?: WeatherInfo;
  weather_info?: WeatherInfo;
  activities?: ActivitiesInfo;
  summary: string;
  final_summary?: string;
  itinerary?: any;
  action_logs?: ActionLogItem[];
  action_log?: string[];
}

export interface PlanTripParams {
  origin?: string;
  destination?: string;
  start_date?: string;
  budget_inr?: number;
  max_budget?: number;
  query?: string;
}

export async function planTrip(params: PlanTripParams): Promise<TripResponse> {
  const rawBackendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
  const BACKEND_URL = rawBackendUrl.replace(/\/+$/, "");

  const payload = {
    origin: params.origin || "DEL",
    destination: params.destination || "GOA",
    start_date: params.start_date || new Date().toISOString().split("T")[0],
    budget_inr: params.budget_inr || params.max_budget || 15000,
    query: params.query || `Plan trip from ${params.origin || "DEL"} to ${params.destination || "GOA"}`
  };

  const response = await fetch(`${BACKEND_URL}/api/plan`, {
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
