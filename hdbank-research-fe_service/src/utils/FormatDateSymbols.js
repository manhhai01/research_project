export const getCurrentDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, '0');
    const day = today.getDate().toString().padStart(2, '0');

    return `${year}-${month}-${day}`;
}

export const getPastAndFutureDates = (currentDate, yearsOffset) => {
    const date = new Date(currentDate);

    const adjustInvalidDate = (d) => {
        if (d.getDate() !== parseInt(d.getDate())) {
            d.setDate(0);
        }
        return d;
    };


    const pastDate = new Date(date);
    pastDate.setFullYear(date.getFullYear() - yearsOffset);
    adjustInvalidDate(pastDate);

    const futureDate = new Date(date);
    futureDate.setFullYear(date.getFullYear() + yearsOffset);
    adjustInvalidDate(futureDate);

    const formatDate = (d) => {
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    return {
        pastDate: formatDate(pastDate),
        futureDate: formatDate(futureDate)
    };
}

export const convertDateFormat = (date) => {
    const [day, month, year] = date.split('-');
    return `${year}-${month}-${day}`;
}
