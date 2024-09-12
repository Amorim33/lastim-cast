import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react/dist/components";
import { ClientOnly } from "remix-utils/client-only";
import { z } from "zod";
import { createDbConnection } from "~/lib/db.server";

import HighchartsReact from "highcharts-react-official";
import Highcharts from "highcharts/highstock";

export async function loader() {
  const db = await createDbConnection();

  const bvspDayIntervalHistoricalData = z
    .array(
      z.object({
        Datetime: z.date(),
        "Adj Close": z.number(),
      })
    )
    .parse(
      await db
        .collection("DayIntervalHistoricalData")
        .find({})
        .project({
          "Adj Close": 1,
          Datetime: 1,
        })
        .sort("Datetime", 1)
        .toArray()
    );

  const bvspDayIntervalPredictedData = z
    .array(
      z.object({
        Datetime: z.date(),
        "Adj Close": z.number(),
      })
    )
    .parse(
      await db
        .collection("DayIntervalPredictedData")
        .find({})
        .project({
          "Adj Close": 1,
          Datetime: 1,
        })
        .sort("Datetime", 1)
        .toArray()
    );

  const historicalData = bvspDayIntervalHistoricalData.map((value) => [
    value.Datetime.getTime(),
    value["Adj Close"],
  ]);
  const predictedData = bvspDayIntervalPredictedData.map((value) => [
    value.Datetime.getTime(),
    value["Adj Close"],
  ]);

  const options: Highcharts.Options = {
    title: {
      text: "^BVSP 1D",
    },
    series: [
      {
        data: historicalData,
        name: "Historical",
        type: "line",
      },
      {
        data: predictedData,
        name: "Predicted",
        type: "line",
      },
    ],
  };

  return json({ options });
}

export default function Day() {
  const { options } = useLoaderData<typeof loader>();
  return (
    <div
      style={{
        width: "90%",
        margin: "0 auto",
      }}
    >
      <ClientOnly fallback={<Fallback />}>
        {() => (
          <HighchartsReact
            highcharts={Highcharts}
            options={options}
            constructorType="stockChart"
          />
        )}
      </ClientOnly>
    </div>
  );
}

function Fallback() {
  return <div>Generating Chart</div>;
}
