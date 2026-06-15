import { ShipmentListResponse } from './types';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchShipments(params: {
  page: number;
  page_size: number;
  origin?: string;
  destination?: string;
  status?: string;
}): Promise<ShipmentListResponse> {
  const queryParams = new URLSearchParams();
  queryParams.set('page', params.page.toString());
  queryParams.set('page_size', params.page_size.toString());

  if (params.origin) {
    queryParams.set('origin', params.origin);
  }
  if (params.destination) {
    queryParams.set('destination', params.destination);
  }
  if (params.status) {
    queryParams.set('status', params.status);
  }

  const response = await fetch(`${BASE_URL}/shipments?${queryParams.toString()}`);

  if (!response.ok) {
    throw new Error('Failed to fetch shipments');
  }

  return response.json();
}
