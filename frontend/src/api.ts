import axios from 'axios';
import { ShipmentListResponse } from './types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function getShipments(params?: {
  status?: string;
  page_size?: number;
  page?: number;
  origin?: string;
  destination?: string;
}): Promise<ShipmentListResponse> {
  const response = await api.get<ShipmentListResponse>('/shipments', {
    params: {
      status: params?.status,
      page_size: params?.page_size,
      page: params?.page,
      origin: params?.origin,
      destination: params?.destination,
    },
  });

  return response.data;
}
