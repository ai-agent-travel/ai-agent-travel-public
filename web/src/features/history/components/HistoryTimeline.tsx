import { getHistoryById } from "../api/getHistoryById";
import type { DayPlan } from "../types";
import { Accomodation } from "@/features/plan/components/Accomodation";
import { Restaurant } from "@/features/plan/components/Restaurant";
import { Spot } from "@/features/plan/components/Spot";
import { ShareButton } from "./ShareButton";

export const HistoryTimeline = async ({ id }: { id: string }) => {
  const history = await getHistoryById(id);

  const dayPlans: DayPlan[] = JSON.parse(history?.content ?? "{}") ?? [];

  return (
    <ul className="timeline timeline-snap-icon timeline-compact timeline-vertical">
      <h1 className="text-2xl font-bold mb-4 border-2 border-primary p-2 rounded-lg shadow-sm flex justify-between items-center">
        {history?.title}
        <ShareButton id={id} />
      </h1>
      {dayPlans.length > 0 &&
        dayPlans.map((item, i) => (
          <li key={item.id}>
            <div className="timeline-middle">
              {/* biome-ignore lint/a11y/noSvgWithoutTitle: <explanation> */}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                className="text-secondary h-8 w-8"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="timeline-end flex flex-col gap-4 mb-10 w-full">
              <h2 className="text-2xl mt-1 ml-2">{i + 1}日目</h2>
              <div className="divider" />
              {/* biome-ignore lint/complexity/useOptionalChain: <explanation> */}
              {item.accommodation && item.accommodation.name && (
                <section className="flex flex-col gap-4">
                  <h3 className="text-lg font-bold">宿泊施設</h3>
                  <Accomodation
                    name={item.accommodation.name}
                    rating={item.accommodation.rating}
                    price={item.accommodation.price}
                    address={item.accommodation.address}
                    description={item.accommodation.description}
                    thumbnail={item.accommodation.thumbnail}
                    hotelImageUrl={item.accommodation.hotel_image_url}
                    dpPlanListUrl={item.accommodation.dp_plan_list_url}
                    hotelSpecial={item.accommodation.hotel_special}
                  />
                </section>
              )}
              <section className="flex flex-col gap-4">
                <h3 className="text-lg font-bold">スポット観光</h3>
                <div className="flex gap-4 carousel">
                  {item.spots.map((spot) => (
                    <Spot key={spot.id} {...spot} />
                  ))}
                </div>
              </section>
              <section className="flex flex-col gap-4">
                <h3 className="text-lg font-bold">ランチ / ディナー</h3>
                <div className="flex gap-4 carousel">
                  {item.lunch && item.lunch.length > 0 && (
                    <Restaurant {...item.lunch[0]} type="lunch" />
                  )}
                  {item.dinner && item.dinner.length > 0 && (
                    <Restaurant {...item.dinner[0]} type="dinner" />
                  )}
                </div>
              </section>
            </div>
            <hr />
          </li>
        ))}
    </ul>
  );
};
