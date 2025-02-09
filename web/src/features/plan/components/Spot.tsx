import { MapPinHouse, Orbit } from "lucide-react";
import { GoogleMapsLink } from "./GoogleMapLink";
import { Rating } from "@smastrom/react-rating";

import "@smastrom/react-rating/style.css";

interface Props {
  id: string;
  name: string;
  address: string;
  thumbnail: string;
  rating: number;
  description: string;
  related_url: string;
  opening_hours: string[];
}

export const Spot = ({
  id,
  name,
  address,
  thumbnail,
  rating,
  related_url,
  description,
  opening_hours,
}: Props) => {
  return (
    <a
      href={related_url}
      className="carousel-item card card-side bg-base-100 border border-gray-200 shadow-sm m-1 hover:shadow-md transition-all duration-300"
      target="_blank"
      rel="noreferrer"
    >
      <div className="w-32 flex items-center justify-center bg-blue-100 rounded-2xl rounded-tr-none rounded-br-none">
        <Orbit size={64} />
      </div>
      <div className="card-body">
        <h2 className="card-title">{name}</h2>
        <div className="flex items-center gap-2">
          <p className="flex items-center gap-2">
            <MapPinHouse size={12} />
            <GoogleMapsLink address={address} />
          </p>
          <p className="text-xs text-gray-500 max-w-48 truncate">
            {opening_hours.join("/")}
          </p>
        </div>
        <p className="text-xs text-gray-500">{description}</p>
        <div className="flex items-center gap-2">
          <Rating value={rating} style={{ maxWidth: 100 }} readOnly />
          <p className="text-xs text-gray-500">{rating} / 5</p>
        </div>
      </div>
    </a>
  );
};
