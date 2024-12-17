import "./Clickable.css"
let Clickable = ({title, onClickFun}) => {

    return (
    <div className="clickable">
    <h1>
        {title}
    </h1>
    <button onClick={onClickFun}>Click me to learn more!</button>
    </div>)
};

export default Clickable;