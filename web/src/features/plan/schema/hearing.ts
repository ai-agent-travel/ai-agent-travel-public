import { z } from "zod";

export const hearingSchema = z.object({
  place: z.string(),
  startDate: z.string(),
  endDate: z.string(),
});

export type Hearing = z.infer<typeof hearingSchema>;
