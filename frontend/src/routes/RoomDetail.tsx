import {
	Avatar,
	Box,
	Button,
	Container,
	Grid,
	GridItem,
	Heading,
	HStack,
	Image,
	Spinner,
	Text,
	VStack,
} from "@chakra-ui/react";
import { FaStar } from "react-icons/fa";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "../calendar.css";
import { checkBooking, getRoom, getRoomReviews } from "../api";
import { IReview, IRoomDetail } from "../types";
import { useState } from "react";
import { Helmet } from "react-helmet";
import {Value} from "react-calendar/dist/shared/types";
import {ICheckBookingResponse} from '../types'

// The type for the value returned by react-calendar when selectRange is true
type DateRange = [Date, Date] | null;

export default function RoomDetail() {
	const { roomPk } = useParams();
	const { isLoading, data } = useQuery<IRoomDetail>({
		queryKey: [`rooms`, roomPk],
		queryFn: getRoom,
	});
	const { data: reviewsData } = useQuery<IReview[]>({
		queryKey: [`rooms`, roomPk, `reviews`],
		queryFn: getRoomReviews,
	});

	const [dates, setDates] = useState<DateRange>(null);


	const onDateChange = (value: Value) => {
		// The `Value` type from react-calendar can be a single Date, an array, or null.
		// We must ensure we are setting a tuple of two dates for our state.
		if (Array.isArray(value) && value.length === 2 && value[0] && value[1]) {
			setDates(value as [Date, Date]);
		}
	};

	const { data: checkBookingData, isLoading: isCheckingBooking } =
		useQuery<ICheckBookingResponse, unknown, ICheckBookingResponse>({
			queryKey: ["check", roomPk!, dates!],
			queryFn: checkBooking,      // context(QueryFunctionContext)를 자동으로 받습니다
			enabled: !!dates,
		});


	const sixMonthsFromNow = new Date();
	sixMonthsFromNow.setMonth(sixMonthsFromNow.getMonth() + 6);

	if (isLoading) {
		return (
			<VStack justifyContent={"center"} minH="100vh">
				<Spinner size="xl" />
			</VStack>
		);
	}

	return (
		<Box
			pb={40}
			mt={10}
			px={{
				base: 10,
				lg: 40,
			}}
		>
			<Helmet>
				<title>{data ? data.name : "Loading..."}</title>
			</Helmet>
			<Heading>{data?.name}</Heading>
			<Grid
				mt={8}
				rounded="xl"
				overflow={"hidden"}
				gap={2}
				height="60vh"
				templateRows={"1fr 1fr"}
				templateColumns={"repeat(4, 1fr)"}
			>
				{/* Display up to 5 photos */}
				{[0, 1, 2, 3, 4].map((index) => (
					<GridItem
						colSpan={index === 0 ? 2 : 1}
						rowSpan={index === 0 ? 2 : 1}
						overflow={"hidden"}
						key={index}
					>
						{data?.photos && data.photos.length > index ? (
							<Image
								objectFit={"cover"}
								w="100%"
								h="100%"
								src={data.photos[index].file}
							/>
						) : (
							<Box bg="gray.100" w="100%" h="100%" />
						)}
					</GridItem>
				))}
			</Grid>
			<Grid gap={20} templateColumns={"2fr 1fr"}>
				<Box>
					<HStack justifyContent={"space-between"} mt={10}>
						<VStack alignItems={"flex-start"}>
							<Heading fontSize={"2xl"}>
								House hosted by {data?.owner.name}
							</Heading>
							<HStack justifyContent={"flex-start"} w="100%">
								<Text>
									{data?.toilets} toilet{data?.toilets === 1 ? "" : "s"}
								</Text>
								<Text>∙</Text>
								<Text>
									{data?.rooms} room{data?.rooms === 1 ? "" : "s"}
								</Text>
							</HStack>
						</VStack>
						<Avatar
							name={data?.owner.name}
							size={"xl"}
							src={data?.owner.avatar}
						/>
					</HStack>
					<Box mt={10}>
						<Heading mb={5} fontSize={"2xl"}>
							<HStack>
								<FaStar /> <Text>{data?.rating}</Text>
								<Text>∙</Text>
								<Text>
									{reviewsData?.length} review
									{reviewsData?.length === 1 ? "" : "s"}
								</Text>
							</HStack>
						</Heading>
						<Container mt={16} maxW="container.lg" marginX="none">
							<Grid gap={10} templateColumns={"1fr 1fr"}>
								{reviewsData?.map((review, index) => (
									<VStack alignItems={"flex-start"} key={index}>
										<HStack>
											<Avatar
												name={review.user.username}
												src={review.user.avatar}
												size="md"
											/>
											<VStack spacing={0} alignItems={"flex-start"}>
												<Heading fontSize={"md"}>{review.user.username}</Heading>
												<HStack spacing={1}>
													<FaStar size="12px" />
													<Text>{review.rating}</Text>
												</HStack>
											</VStack>
										</HStack>
										<Text>{review.payload}</Text>
									</VStack>
								))}
							</Grid>
						</Container>
					</Box>
				</Box>
				<Box pt={10}>
					<Calendar
						onChange={onDateChange}
						value={dates}
						prev2Label={null}
						next2Label={null}
						minDetail="month"
						minDate={new Date()}
						maxDate={sixMonthsFromNow}
						selectRange
					/>
					<Button
						disabled={!checkBookingData?.ok}
						isLoading={isCheckingBooking}
						my={5}
						w="100%"
						colorScheme={"red"}
					>
						Make booking
					</Button>
					{!isCheckingBooking && !checkBookingData?.ok ? (
						<Text color="red.500">Can't book on those dates, sorry.</Text>
					) : null}
				</Box>
			</Grid>
		</Box>
	);
}
