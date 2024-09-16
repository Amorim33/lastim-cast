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

      <main className="flex-grow flex flex-col items-center justify-center text-center px-4">
        <h2 className="text-5xl font-extrabold text-gray-800 mb-6">
          Previsões do Mercado Financeiro
        </h2>
        <p className="text-lg text-gray-600 mb-12">
          Obtenha as previsões mais recentes para o índice ^BVSP em diferentes
          intervalos de tempo.
        </p>
        <div className="flex space-x-6">
          <a
            href="/day"
            className="px-8 py-4 bg-blue-500 text-white rounded-full shadow-lg hover:bg-blue-600 transition duration-300"
          >
            ^BVSP Day Predictions
          </a>
          <a
            href="/hour"
            className="px-8 py-4 bg-green-500 text-white rounded-full shadow-lg hover:bg-green-600 transition duration-300"
          >
            ^BVSP Hour Predictions
          </a>
          <a
            href="/minute"
            className="px-8 py-4 bg-purple-500 text-white rounded-full shadow-lg hover:bg-purple-600 transition duration-300"
          >
            ^BVSP Minute Predictions
          </a>
        </div>
      </main>

      <footer className="text-center p-6 text-gray-500">
        © 2024 LaSTiM Cast. Todos os direitos reservados.
      </footer>
    </div>
  );
}
