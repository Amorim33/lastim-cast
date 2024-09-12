import { MetaFunction } from "@remix-run/node";

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

export default function Index() {
  return (
    <div>
      <h1>LaSTiM Cast Home</h1>
      <nav>
        <ul>
          <li>
            <a href="/day">^BVSP Day Predictions</a>
          </li>
          <li>
            <a href="/hour">^BVSP Hour Predictions</a>
          </li>
          <li>
            <a href="/minute">^BVSP Minute Predictions</a>
          </li>
        </ul>
      </nav>
    </div>
  );
}
