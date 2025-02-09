import Image from "next/image";
import Link from "next/link";

export const Navbar = () => {
  return (
    <div className="navbar bg-base-100 shadow-sm sticky top-0 z-10">
      <label htmlFor="my-drawer" className="btn btn-ghost drawer-button">
        {/* biome-ignore lint/a11y/noSvgWithoutTitle: <explanation> */}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          className="inline-block h-5 w-5 stroke-current"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </label>
      <div className="flex-1">
        <Link href="/home" className="btn btn-ghost text-xl">
          <Image src="/logo.png" alt="AgenTravel" width={25} height={25} />
          AgenTravel
        </Link>
      </div>
    </div>
  );
};
