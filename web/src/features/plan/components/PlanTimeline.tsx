import type { DayPlan } from "../schema";
import { Accomodation } from "./Accomodation";
import { Restaurant } from "./Restaurant";
import { Spot } from "./Spot";

interface Props {
  plans: DayPlan[];
}

export const PlanTimeline = ({ plans }: Props) => {
  return (
    <ul className="timeline timeline-snap-icon timeline-compact timeline-vertical">
      {plans.map((item, i) => (
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
            <section className="flex flex-col gap-4">
              {/* biome-ignore lint/complexity/useOptionalChain: <explanation> */}
              {item?.accommodation && item.accommodation.name && (
                <>
                  <h3 className="text-lg font-bold">宿泊施設</h3>
                  <Accomodation
                    name={item.accommodation.name}
                    address={item.accommodation.address}
                    description={item.accommodation.description}
                    thumbnail={item.accommodation.thumbnail}
                    price={item.accommodation.price}
                    rating={item.accommodation.rating}
                    hotelSpecial={item.accommodation.hotel_special}
                    hotelImageUrl={item.accommodation.hotel_image_url}
                    dpPlanListUrl={item.accommodation.dp_plan_list_url}
                  />
                </>
              )}
            </section>
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
                  <Restaurant
                    name={item.lunch[0].name}
                    type="lunch"
                    address={item.lunch[0].address}
                    thumbnail={item.lunch[0].thumbnail}
                    description={item.lunch[0].description}
                    rating={item.lunch[0].rating}
                    related_url={item.lunch[0].related_url}
                    opening_hours={item.lunch[0].opening_hours}
                  />
                )}
                {item.dinner && item.dinner.length > 0 && (
                  <Restaurant
                    name={item.dinner[0].name}
                    type="dinner"
                    address={item.dinner[0].address}
                    thumbnail={item.dinner[0].thumbnail}
                    description={item.dinner[0].description}
                    rating={item.dinner[0].rating}
                    related_url={item.dinner[0].related_url}
                    opening_hours={item.dinner[0].opening_hours}
                  />
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