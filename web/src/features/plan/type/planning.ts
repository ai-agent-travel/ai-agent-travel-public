import type { Plan } from "../schema";

export type PlanningResponse = {
  current_phase: string;
  form_info: {
    accomodationBudget: string;
    endDate: string;
    people: string;
    place: string;
    startDate: string;
  };
  interrupt: boolean;
  messages: {
    content: string;
    order: number;
    role: string;
    selector: string[];
  }[];
  plans: Plan[];
  thread_id: string;
  user_input_message: string;
};
