import axios from "axios";

export async function POST(req: Request) {
  const body = await req.json();

  const res = await axios({
    method: "POST",
    url: `${process.env.API_ENDPOINT}/agent`,
    data: {
      thread_id: body.thread_id,
      current_phase: body.current_phase,
      user_message: body.user_message,
      user_fbk: body.user_fbk,
      messages: body.messages,
      plans: body.plans,
      form_info: {
        place: body.form_info.place,
        startDate: body.form_info.startDate,
        endDate: body.form_info.endDate,
        accomodationBudget: body.form_info.accomodationBudget,
        people: body.form_info.people,
      },
    },
  });

  return Response.json({
    ...body,
    current_phase: res.data.current_phase,
    messages: res.data.messages,
    user_fbk: res.data.user_fbk,
    user_message: res.data.user_input_message,
    plans: res.data.plans,
  });
}
