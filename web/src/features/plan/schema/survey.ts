import { z } from "zod";

export const surveySchema = z.object({
  place: z.string(),
  startDate: z.string(),
  endDate: z.string(),
  accommodationBudget: z.number(),
  people: z.number(),
});

export type Survey = z.infer<typeof surveySchema>;