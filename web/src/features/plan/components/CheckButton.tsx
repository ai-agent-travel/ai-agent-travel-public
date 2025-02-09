"use client";

import { CheckIcon } from "lucide-react";
import { cn } from "@/lib/utils";

export default function CheckButton({
  className,
  onClick,
}: {
  className?: string;
  onClick?: () => void;
}) {
  return (
    <div className={cn("z-10", className)}>
      <button
        type="button"
        onClick={onClick}
        className="btn btn-circle text-primary mt-2"
      >
        <CheckIcon className="w-4 h-4" />
      </button>
    </div>
  );
}
