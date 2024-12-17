let Error = ({ onClick, counter }) => {
    return (<dialog open>
        <h>
            Unfortunately, what you asked hasn't been implemented yet.
        </h>
        <p>
            Grab a coffee and come back later (good luck with that).
            Times you asked for something I haven't done yet {counter}.
        </p>
        <button onClick={onClick}>
            Click here to reset.
        </button>
    </dialog >)
}

export default Error;