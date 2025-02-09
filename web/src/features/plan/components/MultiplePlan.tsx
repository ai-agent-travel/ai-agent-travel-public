"use client";

import { useState } from "react";
import type { Plan } from "../schema";
import { PlanTimeline } from "./PlanTimeline";
import CheckButton from "./CheckButton";
import CheckDialog from "./CheckDialog";
import { cn } from "@/lib/utils";

interface Props {
  plans: Plan[];
  userId: string;
  reset: () => void;
}

export const MultiplePlan = ({ plans, userId, reset }: Props) => {
  const [checkedPlan, setCheckedPlan] = useState<Plan | null>(null);

  const handleCheck = (plan: Plan) => {
    setCheckedPlan(plan);
    setTimeout(() => {
      (
        document.getElementById("confirm_modal") as HTMLDialogElement
      ).showModal();
    }, 100);
  };

  return (
    <>
      <div className="flex flex-col gap-4">
        {plans?.map((plan, index, array) => (
          <div key={plan.id} className="md:flex gap-4">
            <div className="collapse bg-base-100 border border-base-300">
              <input
                type="checkbox"
                defaultChecked={index === array.length - 1}
              />
              <div className="w-full collapse-title font-semibold flex justify-between items-center">
                {plan.title}
                <CheckButton
                  className="md:hidden"
                  onClick={() => handleCheck(plan)}
                />
              </div>
              <div className="collapse-content">
                <PlanTimeline plans={plan.dayPlans} />
              </div>
            </div>
            <div
              className={cn(
                index === 0 &&
                  "hidden md:block tooltip tooltip-top tooltip-open tooltip-info",
              )}
              data-tip="気に入ったプランを確定する"
            >
              <CheckButton
                className="hidden md:block z-0"
                onClick={() => handleCheck(plan)}
              />
            </div>
          </div>
        ))}
      </div>
      {checkedPlan?.title && (
        <CheckDialog plan={checkedPlan} userId={userId} reset={reset} />
      )}
    </>
  );
};
