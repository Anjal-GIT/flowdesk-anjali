import { Shipment } from './types';

interface ShipmentTableProps {
  shipments: Shipment[];
}

export default function ShipmentTable({ shipments }: ShipmentTableProps) {
  return (
    <table>
      <thead>
        <tr>
          <th>Tracking Code</th>
          <th>Origin</th>
          <th>Destination</th>
          <th>Status</th>
          <th>Weight (kg)</th>
        </tr>
      </thead>
      <tbody>
        {shipments.map((shipment) => (
          <tr key={shipment.id}>
            <td>{shipment.tracking_code}</td>
            <td>{shipment.origin}</td>
            <td>{shipment.destination}</td>
            <td>{shipment.status}</td>
            <td>{shipment.weight_kg}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
