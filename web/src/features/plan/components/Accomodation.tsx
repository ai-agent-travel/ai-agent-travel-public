import { MapPinHouse } from "lucide-react";
import { GoogleMapsLink } from "./GoogleMapLink";
import { Rating } from "@smastrom/react-rating";

interface Props {
  name: string;
  address: string;
  description: string;
  thumbnail: string;
  price: number;
  rating: number;
  hotelImageUrl: string;
  dpPlanListUrl: string;
  hotelSpecial: string;
}

export const Accomodation = ({
  name,
  address,
  description,
  thumbnail,
  price,
  rating,
  hotelImageUrl,
  dpPlanListUrl,
  hotelSpecial,
}: Props) => {
  if (hotelImageUrl === "" || hotelImageUrl.includes("example")) {
    return (
      <p className="text-center text-2xl font-bold text-gray-500">
        適切な宿泊施設が見つかりませんでした。
      </p>
    );
  }
  return (
    <a
      href={dpPlanListUrl}
      className="card card-side flex flex-col md:flex-row border border-gray-200 bg-base-100 shadow-md hover:shadow-lg transition-all duration-300"
      target="_blank"
      rel="noreferrer"
    >
      <figure>
        <img
          src={hotelImageUrl}
          alt={name}
          className="w-64 rounded-xl md:rounded-none h-full"
        />
      </figure>
      <div className="card-body flex flex-col items-start gap-4">
        <div className="w-full card-title flex flex-col md:flex-row items-start justify-between">
          <h2 className="text-2xl">{name}</h2>
          <div className="flex items-center gap-2">
            <Rating value={rating} style={{ maxWidth: 150 }} readOnly />
            <p className="text-sm text-gray-500">{rating} / 5</p>
          </div>
        </div>
        <p>{hotelSpecial}</p>
        <p className="flex items-center gap-2">
          <MapPinHouse />
          <GoogleMapsLink address={address} />
        </p>
        <p className="text-xl font-bold flex items-center gap-2">
          ￥{price} / 泊
        </p>
      </div>
    </a>
  );
};
