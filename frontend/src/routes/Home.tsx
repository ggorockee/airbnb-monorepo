import { Grid } from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { getRooms } from "../api";
import Room from "../components/Room";
import RoomSkeleton from "../components/RoomSkeleton";

interface IPhoto {
	pk: string;
	file: string;
	description: string;
}

export interface IRoom {
	pk: number;
	name: string;
	country: string;
	city: string;
	price: number;
	rating: number;
	is_owner: boolean;
	photos: IPhoto[];
}

export default function Home() {
	const {
		isLoading,
		data: rooms = [],
		error,
	} = useQuery<IRoom[], Error>({
		queryKey: ["rooms"],
		queryFn: getRooms,
	});
	if (error) return <p>에러 발생: {error.message}</p>;

	return (
		<Grid
			mt={10}
			px={{
				base: 10,
				lg: 40,
			}}
			columnGap={4}
			rowGap={8}
			templateColumns={{
				sm: "1fr",
				md: "1fr 1fr",
				lg: "repeat(3, 1fr)",
				xl: "repeat(4, 1fr)",
				"2xl": "repeat(5, 1fr)",
			}}
		>
			{isLoading
				? Array.from({ length: 10 }).map((_, i) => <RoomSkeleton key={i} />)
				: rooms.map((room) => (
					<Room
						key={room.pk}
						pk={room.pk}
						imageUrl={room.photos[0].file}
						name={room.name}
						rating={room.rating}
						city={room.city}
						country={room.country}
						price={room.price}
					/>
				))}
		</Grid>
	);
}