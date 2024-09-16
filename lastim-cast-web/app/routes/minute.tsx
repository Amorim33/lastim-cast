import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react/dist/components";
import { ClientOnly } from "remix-utils/client-only";
import { z } from "zod";
import { createDbConnection } from "~/lib/db.server";

import HighchartsReact from "highcharts-react-official";
import Highcharts from "highcharts/highstock";

export async function loader() {
  const db = await createDbConnection();

  const bvspMinuteIntervalHistoricalData = z
    .array(
      z.object({
        Datetime: z.date(),
        "Adj Close": z.number(),
      })
    )
    .parse(
      await db
        .collection("MinuteIntervalHistoricalData")
        .find({})
        .project({
          "Adj Close": 1,
          Datetime: 1,
        })
        .sort("Datetime", 1)
        .toArray()
    );

  const bvspMinuteIntervalPredictedData = z
    .array(
      z.object({
        Datetime: z.date(),
        "Adj Close": z.number(),
      })
    )
    .parse(
      await db
        .collection("MinuteIntervalPredictedData")
        .find({})
        .project({
          "Adj Close": 1,
          Datetime: 1,
        })
        .sort("Datetime", 1)
        .toArray()
    );

  const historicalData = bvspMinuteIntervalHistoricalData.map((value) => [
    value.Datetime.getTime(),
    value["Adj Close"],
  ]);
  const predictedData = bvspMinuteIntervalPredictedData.map((value) => [
    value.Datetime.getTime(),
    value["Adj Close"],
  ]);

  const options: Highcharts.Options = {
    title: {
      text: "^BVSP 1m",
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

export default function Minute() {
  const { options } = useLoaderData<typeof loader>();
  return (
    <div className="min-h-screen bg-white flex flex-col">
      <header className="flex items-center justify-between p-6">
        <h1 className="text-3xl font-bold text-gray-800">
          <a
            href="/"
            className="text-gray-800 hover:text-blue-500 transition duration-300"
          >
            LaSTiM Cast
          </a>
        </h1>
        <nav>
          <ul className="flex space-x-6">
            <li>
              <a
                href="/day"
                className="text-gray-600 hover:text-blue-500 transition duration-300"
              >
                Dia
              </a>
            </li>
            <li>
              <a
                href="/hour"
                className="text-gray-600 hover:text-green-500 transition duration-300"
              >
                Hora
              </a>
            </li>
            <li>
              <a
                href="/minute"
                className="text-gray-600 hover:text-purple-500 transition duration-300"
              >
                Minuto
              </a>
            </li>
          </ul>
        </nav>
      </header>

      <main className="flex-grow flex items-center justify-center">
        <div className="w-11/12 mx-auto">
          <ClientOnly fallback={<Fallback />}>
            {() => (
              <HighchartsReact
                highcharts={Highcharts}
                options={options}
                constructorType="stockChart"
                containerProps={{ className: "h-full w-full" }}
              />
            )}
          </ClientOnly>
        </div>
      </main>

      <footer className="text-center p-6 text-gray-500">
        © 2024 LaSTiM Cast. Todos os direitos reservados.
      </footer>
    </div>
  );
}

function Fallback() {
  return <div>Generating Chart</div>;
}
