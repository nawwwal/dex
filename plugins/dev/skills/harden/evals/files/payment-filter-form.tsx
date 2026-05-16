export function PaymentFilterForm({ loading, query, onSubmit }: any) {
  return (
    <form
      className="payment-filter"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit(query);
      }}
    >
      <div className="payment-filter__row">
        <input placeholder="Search payments, customers, payment links, invoices, refunds, and settlement IDs" />
        <select defaultValue="all">
          <option value="all">All payment statuses including authorized, captured, failed, refunded, and disputed</option>
        </select>
        <button>Apply filters</button>
      </div>

      {loading ? <p>Loading...</p> : null}
      <p className="payment-filter__error">Invalid date</p>
    </form>
  );
}
