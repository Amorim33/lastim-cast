import { json, MetaFunction } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react/dist/components";
import { ClientOnly } from "remix-utils/client-only";
import { z } from "zod";
import { createDbConnection } from "~/lib/db.server";

import Highcharts from "highcharts/highstock";
import HighchartsReact from "highcharts-react-official";

export const meta: MetaFunction = () => {
  return [
    { title: "Lastim Cast" },
    {
      name: "description",
      content:
        "Predições em tempo real do mercado financeiro brasileiro, utilizando redes neurais do tipo LSTM",
    },
  ];
};

export async function loader() {
  const db = await createDbConnection();

  const bvspDayIntervalHistoricalData = z
    .array(
      z.object({
        Datetime: z.date(),
        Close: z.number(),
      })
    )
    .parse(
      await db
        .collection("DayIntervalHistoricalData")
        .find({})
        .project({
          Close: 1,
          Datetime: 1,
        })
        .sort("Datetime", 1)
        .toArray()
    );

  const data = bvspDayIntervalHistoricalData.map((value) => [
    value.Datetime.getTime(),
    value.Close,
  ]);

  const options: Highcharts.Options = {
    title: {
      text: "^BVSP 1D",
    },
    series: [
      {
        data,
        type: "line",
      },
    ],
  };

  return json({ options });
}

export default function Index() {
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
