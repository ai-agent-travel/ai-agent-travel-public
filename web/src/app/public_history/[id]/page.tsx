import { HistoryTimeline } from "@/features/history/components/HistoryTimeline";
import Image from "next/image";

export default async function History({
  params,
}: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  return (
    <section className="w-full">
      <div className="relative h-40 shadow-lg">
        <Image
          src="/history.webp"
          alt="AI Agent Travel"
          priority
          fill
          className="object-cover"
        />
      </div>
      <div className="md:w-2/3 mt-10 mx-auto p-2">
        <HistoryTimeline id={id} />
      </div>
    </section>
  );
}
