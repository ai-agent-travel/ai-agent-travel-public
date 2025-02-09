"use client";

import { cn } from "@/lib/utils";
import { Share } from "lucide-react";
import { useState } from "react";

interface Props {
  id: string;
}

export const ShareButton = ({ id }: Props) => {
  const [isCopied, setIsCopied] = useState(false);
  const location = window.location.origin;

  return (
    <div
      className={cn(isCopied && "tooltip-open tooltip tooltip-top")}
      data-tip={isCopied ? "URLをコピーしました" : ""}
    >
      <button
        type="button"
        className="btn btn-sm btn-outline"
        onClick={() => {
          navigator.clipboard.writeText(`${location}/public_history/${id}`);
          setIsCopied(true);
          setTimeout(() => {
            setIsCopied(false);
          }, 1000);
        }}
      >
        <Share />
      </button>
    </div>
  );
};