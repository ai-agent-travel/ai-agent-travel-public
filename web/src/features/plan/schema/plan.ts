import { z } from "zod";

const accommodation = z.object({
  id: z.string(),
  name: z.string(),
  address: z.string(),
  thumbnail: z.string(),
  description: z.string(),
  price: z.number(),
  rating: z.number(),
  access: z.string(),
  dp_plan_list_url: z.string(),
  fax_no: z.string(),
  hotel_image_url: z.string(),
  hotel_information_url: z.string(),
  hotel_kana: z.string(),
  hotel_map_image_url: z.string(),
  hotel_no: z.number(),
  hotel_rating_info: z.null(),
  hotel_special: z.string(),
  hotel_thumbnail_url: z.string(),
  latitude: z.number(),
  longitude: z.number(),
  parking_information: z.string(),
  plan_list_url: z.string(),
  postal_code: z.string(),
  review_average: z.number(),
  review_count: z.number(),
  review_url: z.string(),
  room_image_url: z.null(),
  telephone_no: z.string(),
  user_review: z.string(),
});

const spot = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  address: z.string(),
  thumbnail: z.string(),
  rating: z.number(),
  related_url: z.string(),
  opening_hours: z.array(z.string()),
});

const lunch = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  address: z.string(),
  thumbnail: z.string(),
  rating: z.number(),
  related_url: z.string(),
  opening_hours: z.array(z.string()),
});

const dinner = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  address: z.string(),
  thumbnail: z.string(),
  rating: z.number(),
  related_url: z.string(),
  opening_hours: z.array(z.string()),
});

export type Accommodation = z.infer<typeof accommodation>;
export type Spot = z.infer<typeof spot>;
export type Lunch = z.infer<typeof lunch>;
export type Dinner = z.infer<typeof dinner>;

const dayPlan = z.object({
  id: z.string(),
  day: z.number(),
  accommodation: accommodation,
  spots: z.array(spot),
  lunch: z.array(lunch),
  dinner: z.array(dinner),
});

const plan = z.object({
  id: z.string(),
  title: z.string(),
  dayPlans: z.array(dayPlan),
});

export type DayPlan = z.infer<typeof dayPlan>;
export type Plan = z.infer<typeof plan>;
