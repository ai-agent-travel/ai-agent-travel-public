import { MapPinHouse, Utensils, Wine } from "lucide-react";
import { GoogleMapsLink } from "./GoogleMapLink";
import { Rating } from "@smastrom/react-rating";

interface Props {
  name: string;
  type: "lunch" | "dinner";
  address: string;
  thumbnail: string;
  description: string;
  rating: number;
  related_url: string;
  opening_hours: string[];
}

export const Restaurant = ({
  name,
  type,
  address,
  thumbnail,
  description,
  rating,
  related_url,
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
        {type === "lunch" ? <Utensils size={64} /> : <Wine size={64} />}
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
