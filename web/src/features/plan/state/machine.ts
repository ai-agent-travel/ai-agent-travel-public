import { assign, createActor, fromPromise, setup } from "xstate";
import type { Survey, Hearing, Plan } from "../schema";
import { v4 as uuidv4 } from "uuid";

export type Context = {
  threadId: string;
  currentPhase: "phase1" | "phase2" | "phase3";
  userMessage: string;
  userFeedback: string;
  messages: {
    content: string;
    order: number;
    role: string;
    selector: string[];
  }[];
  survey: Survey;
  hearing: Hearing[];
  plans: Plan[];
  loading: boolean;
};

export const initialContext: Context = {
  threadId: uuidv4(),
  currentPhase: "phase1",
  userMessage: "",
  userFeedback: "",
  messages: [],
  survey: {
    place: "",
    startDate: "",
    endDate: "",
    accommodationBudget: 0,
    people: 1,
  },
  hearing: [],
  plans: [],
  loading: false,
};

export const planningMachine = setup({
  types: {
    context: {} as Context,
  },
  actors: {
    submit: fromPromise(async ({ input }: { input: { context: Context } }) => {
      const res = await fetch("/api", {
        method: "POST",
        body: JSON.stringify({
          thread_id: input.context.threadId,
          current_phase: input.context.currentPhase,
          user_message: input.context.userMessage,
          user_fbk: input.context.userFeedback,
          messages: input.context.messages,
          plans: input.context.plans,
          form_info: {
            place: input.context.survey.place,
            startDate: input.context.survey.startDate,
            endDate: input.context.survey.endDate,
            accommodationBudget: input.context.survey.accommodationBudget,
            people: input.context.survey.people,
          },
        }),
      });
      const data = await res.json();

      return {
        ...input.context,
        currentPhase: data.current_phase,
        messages: data.messages,
        userMessage: data.user_input_message,
        userFeedback: data.user_fbk,
        plans: data.plans,
      };
    }),
    reset: fromPromise(async ({ input }: { input: { context: Context } }) => {
      return {
        ...initialContext,
      };
    }),
  },
}).createMachine({
  id: "agent",
  initial: "survey",
  context: initialContext,
  states: {
    reset: {
      invoke: {
        src: "reset",
        input: ({ context }) => ({ context }),
        onDone: {
          target: "survey",
          actions: assign(({ event }) => ({
            ...event.output,
          })),
        },
      },
    },
    survey: {
      on: {
        addPlace: {
          actions: assign({
            survey: ({ context, event }) => ({
              ...context.survey,
              place: event.value,
            }),
          }),
        },
        addStartDate: {
          actions: assign({
            survey: ({ context, event }) => ({
              ...context.survey,
              startDate: event.value,
            }),
          }),
        },
        addEndDate: {
          actions: assign({
            survey: ({ context, event }) => ({
              ...context.survey,
              endDate: event.value,
            }),
          }),
        },
        addAccomodationBudget: {
          actions: assign({
            survey: ({ context, event }) => ({
              ...context.survey,
              accomodationBudget: event.value,
            }),
          }),
        },
        addPeople: {
          actions: assign({
            survey: ({ context, event }) => ({
              ...context.survey,
              people: event.value,
            }),
          }),
        },
        submit: {
          target: "sendSurvey",
        },
      },
    },
    sendSurvey: {
      invoke: {
        src: "submit",
        input: ({ context }) => ({ context }),
        onDone: {
          target: "hearing",
          actions: assign(({ event }) => ({
            ...event.output,
          })),
        },
      },
    },
    hearing: {
      on: {
        addFeedback: {
          actions: assign({
            userMessage: ({ event }) => event.value,
          }),
        },
        submit: {
          target: "sendHearing",
          actions: assign({
            loading: true,
          }),
        },
      },
    },
    sendHearing: {
      invoke: {
        src: "submit",
        input: ({ context }) => ({ context }),
        onDone: {
          target: "checkNext",
          actions: assign(({ event }) => ({
            ...event.output,
            loading: false,
          })),
        },
      },
    },
    checkNext: {
      on: {
        next: [
          {
            guard: ({ context }) => context.currentPhase === "phase1",
            target: "hearing",
          },
          {
            guard: ({ context }) => context.currentPhase === "phase2",
            target: "firstPlanning",
          },
        ],
      },
    },
    firstPlanning: {
      invoke: {
        src: "submit",
        input: ({ context }) => ({ context }),
        onDone: {
          target: "planning",
          actions: assign(({ event }) => ({
            ...event.output,
          })),
        },
      },
    },
    planning: {
      on: {
        addFeedback: {
          actions: assign({
            userFeedback: ({ event }) => event.value,
          }),
        },
        submit: {
          target: "sendPlanning",
          actions: assign({
            loading: true,
          }),
        },
      },
    },
    sendPlanning: {
      invoke: {
        src: "submit",
        input: ({ context }) => ({ context }),
        onDone: {
          target: "planning",
          actions: assign(({ event }) => ({
            ...event.output,
            userFeedback: "",
            loading: false,
          })),
        },
      },
    },
  },
});

export const planningActor = createActor(planningMachine);
