"use client";

export const GoogleMapsLink: React.FC<{ address: string }> = ({ address }) => {
  const encodedAddress = encodeURIComponent(address);
  const googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodedAddress}`;

  const handleClick = () => {
    const newWindow = window.open(
      googleMapsUrl,
      "_blank",
      "noopener,noreferrer",
    );
    if (newWindow) newWindow.opener = null;
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      className="text-blue-600 underline hover:cursor-pointer hover:text-blue-700"
    >
      {address}
    </button>
  );
};
