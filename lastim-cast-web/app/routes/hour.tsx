import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react/dist/components";
import { ClientOnly } from "remix-utils/client-only";
import { z } from "zod";
import { createDbConnection } from "~/lib/db.server";

import HighchartsReact from "highcharts-react-official";
import Highcharts from "highcharts/highstock";

export async function loader() {
  const db = await createDbConnection();

  const bvspHourIntervalHistoricalData = z
    .array(
      z.object({
        Datetime: z.date(),
        "Adj Close": z.number(),
      })
    )
    .parse(
      await db
        .collection("HourIntervalHistoricalData")
        .find({})
        .project({
          "Adj Close": 1,
          Datetime: 1,
        })
        .sort("Datetime", 1)
        .toArray()
    );

  const bvspHourIntervalPredictedData = z
    .array(
      z.object({
        Datetime: z.date(),
        "Adj Close": z.number(),
      })
    )
    .parse(
      await db
        .collection("HourIntervalPredictedData")
        .find({})
        .project({
          "Adj Close": 1,
          Datetime: 1,
        })
        .sort("Datetime", 1)
        .toArray()
    );

  const historicalData = bvspHourIntervalHistoricalData.map((value) => [
    value.Datetime.getTime(),
    value["Adj Close"],
  ]);
  const predictedData = bvspHourIntervalPredictedData.map((value) => [
    value.Datetime.getTime(),
    value["Adj Close"],
  ]);

  const options: Highcharts.Options = {
    title: {
      text: "^BVSP 1H",
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

export default function Hour() {
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
