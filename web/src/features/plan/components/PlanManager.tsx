"use client";

import { InitialForm } from "./InitialForm";
import { Hearing } from "./Hearing";
import { MultiplePlan } from "./MultiplePlan";
import { planningMachine } from "../state/machine";
import { useMachine } from "@xstate/react";
import { useEffect } from "react";
import { snapshotAtomName } from "../state/snapshot";
import { PlanLoading } from "./PlanLoading";
interface Props {
  userId: string;
}

// @ts-ignore
const snapshot = JSON.parse(localStorage.getItem(snapshotAtomName));

export const PlanManager = ({ userId }: Props) => {
  const [state, send] = useMachine(planningMachine, {
    snapshot,
  });

  useEffect(() => {
    localStorage.setItem(snapshotAtomName, JSON.stringify(state));
  }, [state]);

  const resetWithReload = () => {
    localStorage.removeItem(snapshotAtomName);
    window.location.reload();
  };

  const reset = () => {
    localStorage.removeItem(snapshotAtomName);
  };

  return (
    <>
      <div className="-mt-24 mx-auto">
        <InitialForm
          send={send}
          disabled={!state.matches("survey")}
          value={state.context.survey}
        />
      </div>
      {state.matches("sendSurvey") && (
        <div className="flex justify-center items-center my-8">
          <span className="loading loading-dots loading-lg" />
        </div>
      )}
      {!state.matches("survey") && (
        <div className="mx-auto mt-8">
          <Hearing
            messages={state.context.messages.sort((a, b) => a.order - b.order)}
            loading={state.context.loading}
            send={send}
            completed={
              !state.matches("hearing") && !state.matches("sendHearing")
            }
          />
        </div>
      )}
      {state.matches("firstPlanning") && state.context.plans.length === 0 && (
        <PlanLoading
          startDate={state.context.survey.startDate}
          endDate={state.context.survey.endDate}
        />
      )}
      {(state.matches("planning") || state.matches("sendPlanning")) && (
        <>
          <div className="divider" />
          <div className="md:w-2/3 mt-10 mx-auto p-2">
            <MultiplePlan
              userId={userId}
              plans={state.context.plans}
              reset={reset}
            />
          </div>
          {state.matches("sendPlanning") && (
            <div className="mt-4">
              <PlanLoading
                startDate={state.context.survey.startDate}
                endDate={state.context.survey.endDate}
              />
            </div>
          )}
          <div className="md:w-3/5 mt-10 mx-auto p-2">
            <form
              className="flex flex-col md:flex-row gap-6"
              onSubmit={(e) => {
                e.preventDefault();
                send({ type: "submit" });
              }}
            >
              <fieldset className="flex flex-col gap-2 w-full">
                <label htmlFor="feedback flex items-center gap-2">
                  <div className="status status-info status-xl animate-bounce mr-4" />
                  細かい改善ポイントを教えてください！プランを再度作成します！
                </label>
                <textarea
                  id="feedback"
                  placeholder="プランの改善ポイントを教えてください！"
                  className="textarea textarea-secondary w-full text-lg"
                  disabled={state.matches("sendPlanning")}
                  value={state.context.userFeedback}
                  onChange={(e) => {
                    send({ type: "addFeedback", value: e.target.value });
                  }}
                />
              </fieldset>
              <button
                type="submit"
                className="btn btn-secondary mt-auto"
                disabled={state.matches("sendPlanning")}
              >
                プランを再生成
              </button>
            </form>
          </div>
        </>
      )}
      {!state.matches("survey") && (
        <div className="mr-2 md:mr-12 text-right">
          <button
            type="button"
            className="btn btn-outline"
            onClick={resetWithReload}
          >
            リセット
          </button>
        </div>
      )}
    </>
  );
};