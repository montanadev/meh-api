document.addEventListener("DOMContentLoaded", function () {
  const paymentHistoryRows = document.querySelectorAll(
    ".dynamic-payment_history"
  );

  paymentHistoryRows.forEach((row) => {
    const memberProfileInput = row.querySelector(
      "input[name$='member_profile']"
    );
    const userMemberProfileInput = document.querySelector(
      "input[name$='memberprofile_set-0-id']"
    );

    if (memberProfileInput && userMemberProfileInput) {
      memberProfileInput.value = userMemberProfileInput.value;
    }
  });
});