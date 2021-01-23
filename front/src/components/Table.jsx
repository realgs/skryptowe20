import React from "react";
import styled from "styled-components";
import { useTable, usePagination } from "react-table";
import { colors } from "../consts/colors";
import StyledButton from "../components/Button";

const PaginationButton = styled(StyledButton)`
  width: fit-content;
  padding: 0.5rem;
  margin: 1rem 0.25rem;
`;

const Styles = styled.div`
  padding: 1rem;

  table {
    border-spacing: 0;
    border-radius: 5px;
    border: 1px solid black;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;

    tr {
      :last-child {
        td {
          border-bottom: 0;
        }
      }

      :nth-child(odd) {
        background: ${colors.grey};
      }

      :hover {
        background: ${colors.navbarBgContrast};
        color: ${colors.white};
      }
    }

    th {
      background: ${colors.navbarBgColor};
      color: ${colors.white};
    }

    th,
    td {
      margin: 0;
      padding: 0.5rem;
      border-bottom: 1px solid black;
      border-right: 1px solid black;

      :last-child {
        border-right: 0;
      }
    }
  }
`;

function Table({ columns, data }) {
  // Use the state and functions returned from useTable to build your UI
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    page,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    state: { pageIndex, pageSize },
  } = useTable(
    {
      columns,
      data,
      initialState: { pageIndex: 0 },
    },
    usePagination
  );

  // Render the UI for your table
  return (
    <>
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>{column.render("Header")}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map((row, i) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => {
                  return (
                    <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
      <div className="pagination">
        <PaginationButton
          onClick={() => gotoPage(0)}
          disabled={!canPreviousPage}
        >
          {"<<"}
        </PaginationButton>{" "}
        <PaginationButton
          onClick={() => previousPage()}
          disabled={!canPreviousPage}
        >
          {"<"}
        </PaginationButton>{" "}
        <PaginationButton onClick={() => nextPage()} disabled={!canNextPage}>
          {">"}
        </PaginationButton>{" "}
        <PaginationButton
          onClick={() => gotoPage(pageCount - 1)}
          disabled={!canNextPage}
        >
          {">>"}
        </PaginationButton>{" "}
        <span>
          Page{" "}
          <strong>
            {pageIndex + 1} of {pageOptions.length}
          </strong>{" "}
        </span>
        <span>
          | Go to page:{" "}
          <input
            type="number"
            defaultValue={pageIndex + 1}
            onChange={(e) => {
              const page = e.target.value ? Number(e.target.value) - 1 : 0;
              gotoPage(page);
            }}
            style={{ width: "50px" }}
          />
        </span>{" "}
        <select
          value={pageSize}
          onChange={(e) => {
            setPageSize(Number(e.target.value));
          }}
        >
          {[10, 20, 30, 40, 50].map((pageSize) => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
      </div>
    </>
  );
}

const MyTable = ({ data, columns }) => {
  const columnNames = React.useMemo(() => columns, [columns]);

  return (
    <Styles>
      <Table columns={columnNames} data={data} />
    </Styles>
  );
};

export default MyTable;
