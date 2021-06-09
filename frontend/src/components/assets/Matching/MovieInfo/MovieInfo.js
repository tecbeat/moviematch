import React from 'react';
import './MovieInfo.css';
import { AiFillStar } from 'react-icons/ai';

function MovieInfo({
    runtime,
    rating,
    genres,
    tableExtraClasses
}) {
    return (
        <>
            <div className="movieInfo">
                <table className={`movieTable ${tableExtraClasses}`}>
                    <tr>
                        <td className="movieRow">
                            <div>
                                <p className='movieInfoHeader'>Runtime</p>
                                <p className='movieInfoText'>{runtime} minutes</p>
                            </div>
                        </td>
                        <td className="movieRow">
                            <div>
                                <p className='movieInfoHeader'>Rating</p>
                                <p className='movieInfoText'><AiFillStar /> {rating}</p>
                            </div>
                        </td>
                        <td className="movieRow">
                            <div>
                                <p className='movieInfoHeader'>Genres</p>
                                <p className='movieInfoText'>{genres}</p>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
        </>
    )
}

export default MovieInfo;