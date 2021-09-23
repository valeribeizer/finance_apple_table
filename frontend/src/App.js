import React, { useState, useEffect } from "react";
import CssBaseline from "@material-ui/core/CssBaseline";
import Table from "./components/Table";
import axios from "axios";

const App = () => {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/")
      .then((response) => {
        setStocks(response.data);
      })
      .catch((err) => {
        console.log("err");
      });
  }, []);

  const columns = React.useMemo(
    () => [
      {
        Header: "Date",
        accessor: "Date",
      },
      {
        Header: "Open",
        accessor: "Open",
      },
      {
        Header: "High",
        accessor: "High",
      },
      {
        Header: "Low",
        accessor: "Low",
      },
      {
        Header: "Close",
        accessor: "Close",
      },
      {
        Header: "Adj Close",
        accessor: "Adj Close",
      },
      {
        Header: "Volume",
        accessor: "Volume",
      },
    ],
    []
  );

  return (
    <div>
      <CssBaseline />
      <Table columns={columns} data={stocks} />
    </div>
  );
};

export default App;
