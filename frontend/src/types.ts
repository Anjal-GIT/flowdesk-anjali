export interface Shipment {
  id: number;
  tracking_code: string;
  origin: string;
  destination: string;
  status: string;
  weight_kg: number;
  created_at: string;
}

export interface ShipmentListResponse {
  items: Shipment[];
  total: number;
  page: number;
  page_size: number;
}
