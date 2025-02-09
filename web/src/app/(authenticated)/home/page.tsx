import Image from "next/image";
import { cookies } from "next/headers";
import { PlanManager } from "@/features/plan/components/PlanManager";

export default async function Home() {
  const cookieStore = await cookies();
  const userId = cookieStore.get("user.id");

  return (
    <section className="w-full pb-12">
      <div className="relative h-96 shadow-lg">
        <div className="absolute inset-0 h-96">
          <Image
            src="/home.jpg"
            alt="AI Agent Travel"
            priority
            fill
            objectFit="cover"
          />
        </div>
        <h1 className="absolute top-42 left-1/2 transform -translate-x-1/2 -translate-y-1/2 underline decoration-sky-500/30 text-white text-4xl font-bold shadow-accent-content">
          AgenTravel
        </h1>
      </div>
      <PlanManager userId={userId?.value ?? ""} />
    </section>
  );
}
