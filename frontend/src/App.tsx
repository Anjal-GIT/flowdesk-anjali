import { useEffect, useState } from 'react';
import { fetchShipments } from './api';
import { Shipment, ShipmentListResponse } from './types';

const DEFAULT_PAGE_SIZE = 5;

function App() {
  const [shipments, setShipments] = useState<Shipment[]>([]);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(DEFAULT_PAGE_SIZE);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [originFilter, setOriginFilter] = useState('');
  const [destinationFilter, setDestinationFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    loadShipments(page, pageSize);
  }, [page, pageSize]);

  async function loadShipments(pageNumber: number, pageSizeNumber: number) {
    setLoading(true);
    setError(null);

    try {
      const response: ShipmentListResponse = await fetchShipments({
        page: pageNumber,
        page_size: pageSizeNumber,
        origin: originFilter || undefined,
        destination: destinationFilter || undefined,
        status: statusFilter || undefined,
      });

      setShipments(response.items);
      setTotal(response.total);
    } catch (err) {
      setError('Failed to load shipments.');
    } finally {
      setLoading(false);
    }
  }

  function handleSearch() {
    setPage(1);
    loadShipments(1, pageSize);
  }

  function handleClear() {
    setOriginFilter('');
    setDestinationFilter('');
    setStatusFilter('');
    setPage(1);
    loadShipments(1, pageSize);
  }

  return (
    <div className="app-shell">
      <header>
        <h1>Flowdesk Shipments</h1>
        <p>Shipment list page consuming the FastAPI backend.</p>
      </header>

      <section className="filters">
        <div className="field">
          <label htmlFor="origin">Origin</label>
          <input
            id="origin"
            type="text"
            value={originFilter}
            onChange={(event) => setOriginFilter(event.target.value)}
            placeholder="Filter by origin"
          />
        </div>

        <div className="field">
          <label htmlFor="destination">Destination</label>
          <input
            id="destination"
            type="text"
            value={destinationFilter}
            onChange={(event) => setDestinationFilter(event.target.value)}
            placeholder="Filter by destination"
          />
        </div>

        <div className="field">
          <label htmlFor="status">Status</label>
          <select
            id="status"
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="">All statuses</option>
            <option value="pending">Pending</option>
            <option value="in_transit">In Transit</option>
            <option value="delivered">Delivered</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>

        <div className="actions">
          <button onClick={handleSearch}>Search</button>
          <button className="secondary" onClick={handleClear}>Clear</button>
        </div>
      </section>

      <section className="list-card">
        <div className="list-header">
          <div>
            <strong>{total}</strong> shipments found
          </div>
          <div>
            Page {page} / {Math.ceil(total / pageSize) || 1}
          </div>
        </div>

        {loading ? (
          <div className="empty-state">Loading shipments...</div>
        ) : error ? (
          <div className="error-state">{error}</div>
        ) : shipments.length === 0 ? (
          <div className="empty-state">No shipments found.</div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Tracking</th>
                <th>Origin</th>
                <th>Destination</th>
                <th>Status</th>
                <th>Weight (kg)</th>
                <th>Created At</th>
              </tr>
            </thead>
            <tbody>
              {shipments.map((shipment) => (
                <tr key={shipment.id}>
                  <td>{shipment.id}</td>
                  <td>{shipment.tracking_code}</td>
                  <td>{shipment.origin}</td>
                  <td>{shipment.destination}</td>
                  <td>{shipment.status}</td>
                  <td>{shipment.weight_kg}</td>
                  <td>{new Date(shipment.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        <div className="pagination">
          <button
            onClick={() => setPage((current) => Math.max(current - 1, 1))}
            disabled={page === 1}
          >
            Previous
          </button>
          <button
            onClick={() => setPage((current) => current + 1)}
            disabled={page >= Math.ceil(total / pageSize)}
          >
            Next
          </button>
        </div>
      </section>
    </div>
  );
}

export default App;
